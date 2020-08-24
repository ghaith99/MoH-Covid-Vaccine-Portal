import base64
import math
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from barcode.writer import ImageWriter
from barcode import generate
import shortuuid
from mohcovid.utils import send_sms
from pages.models import Patient, SMSNotification, Test, HealthRegion


class TestsQRView(View):

    def get(self, request, pk, *args, **kwargs):  # QR Image generation

        test = Test.objects.get(pk=pk)
        #barcode
        fp = BytesIO()
        generate('code39', pk, writer=ImageWriter(), output=fp)
        fp.seek(0)

        #QR Code
        img = qrcode.make(str(test.id))
        canvas = Image.new('RGB', (350, 370), 'white')
        ImageDraw.Draw(canvas)
        canvas.paste(img)
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        canvas.close()
        buffer.seek(0)
        
        return render(
            request, 'qrcode.html', {
                'qrcode': (base64.b64encode(buffer.read()).decode()),
                'test' : test,
                'sample_date': test.sample_datetime.strftime("%Y-%m-%d"),
                'patient': test.patient,
                'barcode': (base64.b64encode(fp.read()).decode())
            }
        )

class HomePageView(LoginRequiredMixin, TemplateView):
    model = Test
    template_name = 'home.html'
    login_url = 'login'


# Tests Views
class TestsListView(LoginRequiredMixin, ListView):
    template_name = "tests_list.html"
    login_url = 'login'
    model = Test

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['health_regions'] = HealthRegion.objects.all()
        context['test_result_choices'] = [x for x,y in Test._meta.get_field('test_result').choices]
        
        return context

    def get_queryset(self):  # Filter Patients
        health_region = None
        test_result = None
        result_datetime = None
        
        health_region = self.request.GET.get('health_region') 
        test_result =  self.request.GET.get('test_result')
        if self.request.GET.get('result_datetime'):
            result_datetime =  datetime.strptime(self.request.GET.get('result_datetime'), "%Y-%m-%d")

        print(result_datetime)
        # query = self.request.GET.get('test')

        object_list = self.model.objects.all().order_by('-sample_datetime') 

        if health_region:
            object_list = object_list.filter(
                patient__area__health_region__name = health_region
            ).order_by('sample_datetime')
        if test_result:
            object_list = object_list.filter(
                test_result = test_result
            ).order_by('sample_datetime')
        if result_datetime:
            object_list = object_list.filter(
                result_datetime__year = result_datetime.year,
                result_datetime__month = result_datetime.month,
                result_datetime__day = result_datetime.day,
            ).order_by('sample_datetime')
        
        # if query:
        #     object_list = object_list.filter(
        #         pk=query
        #     ).order_by('sample_datetime')
         

        paginator = Paginator(object_list, 10)
        page = self.request.GET.get('page')
        if page and page != "":
            tests = paginator.get_page(page)
            print(tests)
        else:
            tests = paginator.get_page(1)
        return tests


class TestsPagination(View):

    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        total = tests.count()
        page = 1
        per_page = 2
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1
            per_page = length

            tests = tests[start:start + length]

        data = [test.to_dict_json() for test in tests]
        response = {
            'data': data,
            'page': page,  # [optional]
            'per_page': per_page,  # [optional]
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context


class TestCreateView(LoginRequiredMixin,  CreateView):
    # form_class = TestCreateForm
    template_name = 'test_new.html'
    login_url = 'login'
    model = Test
    fields = '__all__'

    def get_initial(self):  # auto populate patient if GET request with id
        initial = super(TestCreateView, self).get_initial()
        query = self.request.GET.get('id')
        if query:
            initial['patient'] = Patient.objects.get(id=query)
        return initial

    # override to inject roles to fields visibility
    # before form_class() calls form factory
    def get_form(self, form_class=None):

        if self.request.user.role == 'Admin':
            self.fields = [
                'patient', 'test_result', 'result_datetime',
                'symptoms', 'mixed', 'lab_doctor',
                'screening_center', 'testing_center', 'test_notes'
            ]
        elif self.request.user.role == 'Lab':
            self.fields = [
                'patient', 'test_result', 'symptoms', 'mixed', 'lab_doctor',
                'screening_center', 'testing_center', 'test_notes'
            ]
        elif self.request.user.role == 'Field':
            self.fields = ['patient', 'screening_center', 'symptoms', 'mixed']

        if form_class is None:
            form_class = self.get_form_class()
        # pass to the new form the fields defined
        form = form_class(**self.get_form_kwargs())

        if self.request.user.role in ('Field', 'Lab'):
            form.fields['patient'].disabled = True

        # result_datetime = forms.DateTimeField(input_formats=['%d/%m/%Y'])
        # patient = forms.CharField()
        # sample_datetime = forms.DateTimeField(input_formats=['%d/%m/%Y'])
        return form

    def form_valid(self, form):  # bind author of the test + set result time
        test = form.save(commit=False)

        # bind test to user
        test.author = self.request.user
        
        # update result time on result update + the person
        # who updates the lab result is the doctor
        if test.test_result is not None:
            test.result_datetime = datetime.now()
            test.lab_doctor = self.request.user
            obj = SMSNotification.objects.create(test=test, message='negative')
            send_sms([obj], 1)
        
        test.save()

        return super().form_valid(form)  # rediret to detailview


class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Test
    template_name = 'test_edit.html'
    fields = []
    login_url = 'login'

    # override to inject roles to fields visibility
    # before form_class() calls form factory
    def get_form(self, form_class=None):
        if self.request.user.role == 'Admin':
            self.fields = [
                'patient', 'test_result', 'result_datetime',
                'symptoms', 'mixed', 'lab_doctor', 'testing_center',
                'screening_center', 'test_notes'
            ]
        elif self.request.user.role == 'Lab':
            self.fields = [
                'test_result', 'symptoms', 'mixed', 'lab_doctor',
                'testing_center', 'screening_center', 'test_notes'
            ]
        elif self.request.user.role == 'Field':
            self.fields = ['symptoms', 'mixed']
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        return form

    def form_valid(self, form):
        test = form.save(commit=False)
        # if result is updated then set the current time to the result date
        if test.test_result is not None:
            test.result_datetime = datetime.now()
            test.lab_doctor = self.request.user
            obj, _ = SMSNotification.objects.get_or_create(
                test=test,
                sent_status=False
            )
            obj.message = test.test_result
            obj.save()
            send_sms([obj], 1)
        test.save()
        return super().form_valid(form)  # rediret to detailview


class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = 'test_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

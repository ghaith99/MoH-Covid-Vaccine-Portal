import base64
import math
from datetime import datetime
from io import BytesIO

import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from PIL import Image, ImageDraw

from mohcovid.utils import send_sms
from pages.models import Patient, SMSNotification, Test


class TestsQRView(View):

    def get(self, request, pk, *args, **kwargs):  # QR Image generation

        test = Test.objects.get(pk=pk)
        print(str(test.id))
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
                'sample_date': test.sample_datetime.strftime("%Y-%m-%d")
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

    def get_queryset(self):  # Filter Patients
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                pk=query
            ).order_by('sample_datetime')
        else:
            if self.request.user.role == 'Admin':
                object_list = self.model.objects.all()
            else:
                object_list = self.model.objects.filter(
                    author=self.request.user
                ).order_by('-sample_datetime')  # filter on user tests only

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
        test.save()
        obj = SMSNotification.objects.create(test=test, message='negative')
        send_sms([obj], 1)
        # confirm doctor is specified when updating the result
        # if(test.lab_doctor is None and test.test_result is not None ):
        #     form.add_error(
        #         'lab_doctor',
        #         "Lab Doctor has to be set to update the result."
        #     )
        #     return super().form_invalid(form)

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
        print('hereeee')
        test = form.save(commit=False)
        # if result is updated then set the current time to the result date
        if test.test_result is not None:
            test.result_datetime = datetime.now()
            test.lab_doctor = self.request.user
        test.save()
        obj, _ = SMSNotification.objects.get_or_create(
            test=test,
            sent_status=False
        )
        obj.message = test.test_result
        obj.save()
        print('here')
        send_sms([obj], 1)
        return super().form_valid(form)  # rediret to detailview


class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = 'test_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

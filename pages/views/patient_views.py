from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
import requests, json
from django.shortcuts import redirect
from datetime import datetime
from django import forms
from django.db import models
from mohcovid.utils import checkandSendSMS
from ..models import Test, Patient
from django.shortcuts import render

class TestsQRView(View):
    
    def get(self, request, pk, *args, **kwargs):
        test = Test.objects.get(pk=pk)
        return render(request, "qrcode.html", {'qrcode': test.qr_code.url,
        'sample_date':test.sample_datetime.strftime("%Y-%m-%d")})

class HomePageView(LoginRequiredMixin, TemplateView):
    model = Test
    template_name = 'home.html'
    login_url = 'login'

## Tests Views
class TestsListView(LoginRequiredMixin, ListView):
    template_name = "tests_list.html"
    login_url = 'login'
    model = Test
    def get_queryset(self): #Filter Patients
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(id=query)
            return object_list
        else: 
            if self.request.user.role == 'Admin':
                return self.model.objects.all()
            return self.model.objects.filter(author=self.request.user)

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context
    

class TestCreateView(LoginRequiredMixin,  CreateView):
    result_datetime = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    model = Test
    template_name = 'test_new.html'
    login_url = 'login'
    fields = []
    
    def get_initial(self): #auto populate patient if GET request with id
   
        initial = super(TestCreateView, self).get_initial()
        query = self.request.GET.get('id')
        if query:
            initial['patient'] = Patient.objects.get(id=query)
        return initial

    def get_form(self, form_class=None): #override to inject roles to fields visibility before form_class() calls form factory
        if self.request.user.role == 'Admin':
            self.fields = ['patient', 'test_result', 'result_datetime', 'symptoms', 'mixed', 'lab_doctor', 'testing_center','test_notes', 'completed']
        elif self.request.user.role == 'Lab':
            self.fields = ['patient', 'test_result', 'result_datetime', 'symptoms', 'mixed', 'lab_doctor', 'testing_center','test_notes', 'completed']
        elif self.request.user.role == 'Field':
            self.fields = ['patient', 'sampling_datetime', 'symptoms', 'mixed', ]

        if form_class is None:
            form_class = self.get_form_class()
        
        form = form_class(**self.get_form_kwargs())
        return form
        
    def form_valid(self, form): #bind author of the test
        print("Form Valid")
        test = form.save(commit=False)
        test.author = self.request.user
        test.save()
        return super().form_valid(form) # rediret to detailview

class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Test
    template_name = 'test_edit.html'
    fields = []
    login_url = 'login'

    def get_form(self, form_class=None): #override to inject roles to fields visibility before form_class() calls form factory
        if self.request.user.role == 'Admin':
            self.fields = ['patient', 'test_result', 'result_datetime', 'symptoms', 'mixed', 'lab_doctor', 'testing_center','test_notes', 'completed',]
        elif self.request.user.role == 'Lab':
            self.fields = ['test_result', 'result_datetime', 'symptoms', 'mixed','lab_doctor', 'testing_center', 'test_notes', 'completed',]
        elif self.request.user.role == 'Field':
            self.fields = ['symptoms', 'mixed', ]

        if form_class is None:
            form_class = self.get_form_class()
        
        form = form_class(**self.get_form_kwargs())
        return form

class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = 'test_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

##Patients Views
class PatientsListView(LoginRequiredMixin, ListView):
    template_name = "patients_list.html"
    login_url = 'login'
    model = Patient
    
    def get_queryset(self): #Searchbar Filter Patients
        query = self.request.GET.get('q')
        if query:          
            object_list = self.model.objects.filter(civil_ID=query)
            return object_list
        else: 
            if self.request.user.role == 'Admin':
                return self.model.objects.all()
            return self.model.objects.filter(author=self.request.user)
    
class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    login_url = 'login'
    
class PatientCreateForm(forms.ModelForm):
    YES_NO = (
        ('No', 'No'),
        ('Yes', 'Yes'),
    )
    mixed = forms.CharField(widget=forms.Select(choices=YES_NO),max_length=3)
    symptoms = forms.CharField(widget=forms.Select(choices=YES_NO),max_length=3)

    class Meta:
        model = Patient
        fields = ["civil_ID", "phone","comments"]
    
class PatientCreateView(LoginRequiredMixin, CreateView):
    
    template_name = 'patient_new.html'
    login_url = 'login'
    form_class = PatientCreateForm
    
    def form_valid(self, form):
        patient = form.save(commit=False)
        try:
            x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':form['civil_ID'].value()})
            if (x.status_code == 200):
                patientData =  json.loads(x.text)  
                patient.city = patientData['PR_DISTRICT']
                patient.civil_serial = patientData['PR_SERIAL_NO']
                patient.birthday = datetime.strptime(patientData['PR_BIRTH_DATE'],"%Y%M%d")
                patient.first_name = patientData['PR_ARAB_NAME1']
                patient.last_name = patientData['PR_ARAB_NAME2']+" "+ patientData['PR_ARAB_NAME3']+" "+patientData['PR_ARAB_NAME4']
                patient.nationality = patientData['PR_NATIONALITY']
                patient.gender = patientData['PR_SEX']
                patient.author = self.request.user
                patient.save()

                test = Test(author = self.request.user)
                test.patient = patient
                test.mixed = form['mixed'].value()
                test.symptoms = form['symptoms'].value()
                test.save()

                #checkandSendSMS.delay()
            else:
                form.add_error('civil_ID', "Civil ID is Wrong!")
                return super().form_invalid(form)
        except Exception as e:
            print("error=====================================")
            print(e)
            form.add_error(None, "Form Processing Error")
            return super().form_invalid(form)

        return super().form_valid(form) # rediret to detailview

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient_edit.html'
    fields = ["phone","comments"]
    login_url = 'login'

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
import requests, json
from django.shortcuts import redirect
from datetime import datetime
from django import forms

from mohcovid.utils import checkandSendSMS

from .models import Test, Patient

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
    
class TestCreateView(LoginRequiredMixin, CreateView):
    resultDate = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    model = Test
    template_name = 'test_new.html'
    fields = ['patient', 'testResult', 'resultDate', 'testNotes', ]
    login_url = 'login'
    
    def get_initial(self): #auto populate patient from GET id
        initial = super(TestCreateView, self).get_initial()
        query = self.request.GET.get('id')
        if query:
            initial['patient'] = Patient.objects.get(id=query)
        return initial
 
    def form_valid(self, form): #bind author of the test
        test = form.save(commit=False)
        test.author = self.request.user
        test.save()
        return super().form_valid(form) # rediret to detailview


class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Test
    template_name = 'test_edit.html'
    fields = ['resultDate', 'testResult','testNotes',]
    login_url = 'login'


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
            object_list = self.model.objects.filter(civilID=query)
            return object_list
        else: 
            if self.request.user.role == 'Admin':
                return self.model.objects.all()
            return self.model.objects.filter(author=self.request.user)
    
class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    login_url = 'login'
    
class PatientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'patient_new.html'
    login_url = 'login'
    model = Patient
    fields = ["civilID", "phone", "status","comments"]

    def form_valid(self, form):
        patient = form.save(commit=False)
        try:
            #Patient exists, redirect to the updateView
            #p = Patient.objects.filter(civilID=form['civilID'].value())
            #print(p)
            # if(len(p) == 1):
            #     print("found")
            #     return reverse('patient_edit', args=(str(p[0].id)))
            #New Patient    
            x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':form['civilID'].value()})
            if (x.status_code == 200):
                patientData =  json.loads(x.text)  
                print(patientData) 
                patient.city = patientData['PR_DISTRICT']
                patient.civilSerial = patientData['PR_SERIAL_NO']
                patient.birthday = datetime.strptime(patientData['PR_BIRTH_DATE'],"%Y%M%d")
                patient.firstname = patientData['PR_ARAB_NAME1']
                patient.lastname = patientData['PR_ARAB_NAME2']+patientData['PR_ARAB_NAME3'] + patientData['PR_ARAB_NAME4']
                patient.nationality = patientData['PR_NATIONALITY']
                patient.gender = patientData['PR_SEX']
                patient.author = self.request.user
                patient.save()

                # test = Test(author = self.request.user)
                # test.patient = patient
                # test.save()
                #checkandSendSMS.delay()
            else:
                form.add_error('civilID', "Civil ID is Wrong!")
                return super().form_invalid(form)
        except Exception as e:
            print(e)
            form.add_error(None, "Connection Error")
            return super().form_invalid(form)

        return super().form_valid(form) # rediret to detailview


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient_edit.html'
    fields = ["civilID", "civilSerial", "phone", "status","comments"]
    login_url = 'login'

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
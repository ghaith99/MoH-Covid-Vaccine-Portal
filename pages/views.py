from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
import requests, json

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
 
    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Test.objects.all()
        return Test.objects.filter(author=self.request.user)


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'
    login_url = 'login'
    
class TestCreateView(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'test_new.html'
    fields = '__all__'
    login_url = 'login'

class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Test
    template_name = 'test_edit.html'
    fields = ['resultDate', 'testNotes', 'testResult', 'author']
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

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Patient.objects.all()
        return Patient.objects.filter(author=self.request.user)

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    login_url = 'login'
    
class PatientCreateView(LoginRequiredMixin, CreateView):

    template_name = 'patient_new.html'
    login_url = 'login'
    model = Patient
    fields = ["civilID", "civilSerial", "phone", "status","comments"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':form['civilID'].value()})
        if (x.status_code == 200):
            patientData =  json.loads(x.text)        
            print(patientData['PR_DISTRICT'])
            obj.city = patientData['PR_DISTRICT']
            obj.save()
            checkandSendSMS.delay()
        else:
            form.add_error('civilID', "Civil ID is Wrong!")
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
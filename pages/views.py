from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 


from .models import Test, Patient

class HomePageView(TemplateView):
    model = Test
    template_name = 'home.html'

## Tests Views
class TestsListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = "tests_list.html"
    login_url = 'login'

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'
    login_url = 'login'
    
class TestCreateView(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'test_new.html'
    fields = ['patient','resultDate', 'testNotes', 'testResult', 'completed', 'hospital', 'author']
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
    model = Patient
    template_name = "patients_list.html"
    login_url = 'login'

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    login_url = 'login'
    

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'patient_new.html'
    fields = ["civilID", "civilSerial", "firstname", "lastname", "gender", "birthday", "city", "symptoms", "phone", "bloodType","allergy","alzheimer","asthma","diabetes","stroke","comments"]
    login_url = 'login'


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient_edit.html'
    fields = ["civilID", "civilSerial", "firstname", "lastname", "gender", "birthday", "city", "symptoms", "phone", "bloodType","allergy","alzheimer","asthma","diabetes","stroke","comments"]
    login_url = 'login'

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
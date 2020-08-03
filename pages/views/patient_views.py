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
from django.core.paginator import Paginator

##Patients Views
class PatientsListView(LoginRequiredMixin, ListView):
    template_name = "patients_list.html"
    login_url = 'login'
    model = Patient
    
    def get_queryset(self): #Searchbar Filter Patients
        query = self.request.GET.get('q')
        if query:          
            object_list = self.model.objects.filter(civil_ID=query)
        else: 
            if self.request.user.role == 'Admin':
                object_list =  self.model.objects.all()
            else:
                object_list = self.model.objects.filter(author=self.request.user)
        
        paginator = Paginator(object_list, 10)
        page = self.request.GET.get('page')
        if page and page != "":
            patients = paginator.get_page(page)
            print(patients)
        else:
            patients = paginator.get_page(1)
        
        print(object_list)

        return patients
    
class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    login_url = 'login'
    
class PatientCreateView(LoginRequiredMixin, CreateView):
    
    template_name = 'patient_new.html'
    login_url = 'login'
    model = Patient
    fields = ["civil_ID", "phone","comments"]
    
    def form_valid(self, form):
        patient = form.save(commit=False)
        try:
            x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':form['civil_ID'].value()},  verify=False)
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


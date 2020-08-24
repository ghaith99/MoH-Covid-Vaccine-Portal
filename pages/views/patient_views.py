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
from mohcovid.utils import send_sms
from ..models import Test, Patient
from ..filters import PatientFilter
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q


class CheckPatientCivilID(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        civil_id = request.GET.get('civil_id')

        x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':civil_id},  verify=False)
        if (x.status_code == 200):
            patientData =  json.loads(x.text)  
            # patient = Patient.objects.get_or_create(civil_ID=civil_id, author = self.request.user)
            print(patientData)
            response = {
                'civil_ID': patientData['PR_CIVNO'],
                'city': patientData['PR_DISTRICT'],
                'civil_serial': patientData['PR_SERIAL_NO'],
                #'birthday': datetime.strptime(patientData['PR_BIRTH_DATE'], "%Y%M%d"),  
                'first_name': patientData['PR_ARAB_NAME1'],
                'last_name': patientData['PR_ARAB_NAME2'] + " " + patientData['PR_ARAB_NAME3']+" "+patientData['PR_ARAB_NAME4'],
                'nationality': patientData['PR_NATIONALITY'],
                'gender': "M" if patientData['PR_SEX'] == 'ذكر' else "F"
            }

        return JsonResponse(response)


##Patients Views
class PatientsListView(LoginRequiredMixin, ListView):
    template_name = "patients_list.html"
    login_url = 'login'
    model = Patient
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       #context['filter'] = PatientFilter(self.request.GET, queryset=Patient.objects.all())

        context['total_patients'] = Patient.objects.all().count()
       
        return context

    def get_queryset(self): #Searchbar Filter Patients
        object_list =  self.model.objects.all()

        query = self.request.GET.get('q')
        if query:          
            object_list = self.model.objects.filter( Q(civil_ID__contains=query)     | Q(first_name__contains=query)\
                                                | Q(nationality__contains=query)     | Q(gender__contains=query)\
                                                | Q(first_name__contains=query)      | Q(last_name__contains=query)\
                                                | Q(phone__contains=query)           | Q(city__contains=query)\
                                                | Q(passport_number__contains=query) | Q(id__contains=query))
        # else: 
        #     if self.request.user.role == 'Admin':
        #         object_list =  self.model.objects.all()
        #     else:
        #         object_list = self.model.objects.filter(author=self.request.user)
         
        paginator = Paginator(object_list, 10)
        page = self.request.GET.get('page')
        if page and page != "":
            patients = paginator.get_page(page)
            print(patients)
        else:
            patients = paginator.get_page(1)
        
        return patients
    
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
        fields = ["civil_ID", "first_name", "last_name", "area", "nationality", "gender", "phone"]

class PatientCreateView(LoginRequiredMixin, CreateView):   
    template_name = 'patient_new.html'
    form_class = PatientCreateForm
    login_url = 'login'
    model = Patient

    # def get_form(self, form_class=None):
    #     mixed = forms.CharField(widget=forms.Select(choices=(('False','False'), ('True', 'True'))))
    #     symptoms = forms.CharField(widget=forms.Select(choices=(('False','False'), ('True', 'True'))))

    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     form = form_class(**self.get_form_kwargs()) #pass to the new form the fields defined

    #     return form

    def form_valid(self, form):
        patient = form.save(commit=False)
        try:
            x = requests.post('https://cpkw.org/api/moh_mock/', {'civil_id':form['civil_ID'].value()},  verify=False)
            if (x.status_code == 200):
                patientData =  json.loads(x.text)  
                print(patientData)
                patient.city = patientData['PR_DISTRICT']
                patient.civil_serial = patientData['PR_SERIAL_NO']
                patient.birthday = datetime.strptime(patientData['PR_BIRTH_DATE'], "%Y%M%d")
                patient.first_name = patientData['PR_ARAB_NAME1']
                patient.last_name = patientData['PR_ARAB_NAME2'] + " " + patientData['PR_ARAB_NAME3']+" "+patientData['PR_ARAB_NAME4']
                patient.nationality = patientData['PR_NATIONALITY']
                patient.gender = patientData['PR_SEX']
                patient.author = self.request.user
                patient.save()

                test = Test()
                test.author = self.request.user
                test.patient = patient
                test.mixed = form['mixed'].value()
                test.symptoms = form['symptoms'].value()
                test.save()

            else:
                form.add_error('civil_ID', "Civil ID is Wrong!")
                return super().form_invalid(form)
        except Exception as e:
            print("error=====================================")
            print(e)
            form.add_error(None, "Form Processing Error")
            return super().form_invalid(form)

        if(self.request.user.role == 'Field'):
            return HttpResponseRedirect(reverse("test_qrcode",kwargs={'pk': test.pk}))

        return super().form_valid(form) # rediret to detailview


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient_edit.html'
    fields = ["phone","civil_ID", "area","first_name","last_name", "comments"]
    login_url = 'login'


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

#Screening Center Views
from ..models import ScreeningCenter
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
from django.shortcuts import render

class ScreeningCentersListView(ListView):
    model = ScreeningCenter
    template_name = 'screeningcenters_list.html'

class ScreeningCenterDetailView(DetailView):
    model = ScreeningCenter
    template_name = 'screeningcenter_detail.html'
    fields = "__all__"

class ScreeningCenterCreateView(CreateView):
    model = ScreeningCenter
    template_name = 'screeningcenter_new.html'
    fields = "__all__"

class ScreeningCenterUpdateView(UpdateView):
    model = ScreeningCenter
    template_name = 'screeningcenter_edit.html'
    fields = "__all__"

class ScreeningCenterDeleteView(DeleteView):
    model = ScreeningCenter
    template_name = 'screeningcenter_delete.html'
    success_url = reverse_lazy('home')

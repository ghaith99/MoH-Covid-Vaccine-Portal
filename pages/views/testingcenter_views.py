#Testing Center Views
from ..models import TestingCenter
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

class TestingCentersListView(ListView):
    model = TestingCenter
    template_name = 'testingcenters_list.html'

class TestingCenterDetailView(DetailView):
    model = TestingCenter
    template_name = 'testingcenter_detail.html'
    fields = "__all__"

class TestingCenterCreateView(CreateView):
    model = TestingCenter
    template_name = 'testingcenter_new.html'
    fields = "__all__"

class TestingCenterUpdateView(UpdateView):
    model = TestingCenter
    template_name = 'testingcenter_edit.html'
    fields = "__all__"

class TestingCenterDeleteView(DeleteView):
    model = TestingCenter
    template_name = 'testingcenter_delete.html'
    success_url = reverse_lazy('home')

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 


from .models import Test, Citizen

class HomePageView(TemplateView):
    model = Test
    template_name = 'home.html'

class TestsListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = "tests.html"
    login_url = 'login'

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'

class TestCreateView(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'test_new.html'
    fields = ['resultDate', 'testNotes', 'testResult', 'author']
    login_url = 'login'

class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Test
    template_name = 'test_edit.html'
    fields = ['resultDate', 'testNotes', 'testResult', 'author']

class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = 'test_delete.html'
    success_url = reverse_lazy('home')

    
from django.urls import path

from .views import HomePageView, TestsListView, TestDetailView, TestCreateView, TestDeleteView, TestUpdateView, PatientsListView, PatientDetailView, PatientCreateView, PatientDeleteView, PatientUpdateView
from django.views.generic.base import TemplateView

urlpatterns = [
        path('test/<int:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),
        path('test/<int:pk>/edit/', TestUpdateView.as_view(), name='test_edit'),
        path('test/new', TestCreateView.as_view(), name='test_new'),
        path('test/<int:pk>', TestDetailView.as_view(), name='test_detail'),
        path('tests/', TestsListView.as_view(), name='tests_list'),
        
        path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
        path('patient/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient_edit'),
        path('patient/new', PatientCreateView.as_view(), name='patient_new'),
        path('patient/<int:pk>', PatientDetailView.as_view(), name='patient_detail'),
        path('patients/', PatientsListView.as_view(), name='patients_list'),
      
        path('', HomePageView.as_view(), name='home'),
]

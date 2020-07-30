from django.urls import path, include

from .views import HomePageView, TestsListView, TestDetailView, TestCreateView, TestDeleteView, TestUpdateView, PatientsListView, PatientDetailView, PatientCreateView, PatientDeleteView, PatientUpdateView, TestsQRView, ScreeningCenterDeleteView,ScreeningCenterUpdateView,ScreeningCenterCreateView,ScreeningCenterDetailView,ScreeningCentersListView, TestingCenterDeleteView,TestingCenterUpdateView,TestingCenterCreateView,TestingCenterDetailView,TestingCentersListView

from django.views.generic.base import TemplateView

urlpatterns = [
        path('test/<uuid:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),
        path('test/<uuid:pk>/edit/', TestUpdateView.as_view(), name='test_edit'),
        path('test/new/', TestCreateView.as_view(), name='test_new'),
        path('test/<uuid:pk>', TestDetailView.as_view(), name='test_detail'),
        path('tests/', TestsListView.as_view(), name='tests_list'),
        path('test/<uuid:pk>/qrcode', TestsQRView.as_view(), name='test_qrcode'),

        path('patient/<uuid:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
        path('patient/<uuid:pk>/edit/', PatientUpdateView.as_view(), name='patient_edit'),
        path('patient/new', PatientCreateView.as_view(), name='patient_new'),
        path('patient/<uuid:pk>', PatientDetailView.as_view(), name='patient_detail'),
        path('patients/', PatientsListView.as_view(), name='patients_list'),
      
        path('screeningcenter/<uuid:pk>/delete/', ScreeningCenterDeleteView.as_view(), name='screeningcenter_delete'),
        path('screeningcenter/<uuid:pk>/edit/', ScreeningCenterUpdateView.as_view(), name='screeningcenter_edit'),
        path('screeningcenter/new', ScreeningCenterCreateView.as_view(), name='screeningcenter_new'),
        path('screeningcenter/<uuid:pk>', ScreeningCenterDetailView.as_view(), name='screeningcenter_detail'),
        path('screeningcenters/', ScreeningCentersListView.as_view(), name='screeningcenters_list'),
        
        path('testingcenter/<uuid:pk>/delete/', TestingCenterDeleteView.as_view(), name='testingcenter_delete'),
        path('testingcenter/<uuid:pk>/edit/', TestingCenterUpdateView.as_view(), name='testingcenter_edit'),
        path('testingcenter/new', TestingCenterCreateView.as_view(), name='testingcenter_new'),
        path('testingcenter/<uuid:pk>', TestingCenterDetailView.as_view(), name='testingcenter_detail'),
        path('testingcenters/', TestingCentersListView.as_view(), name='testingcenters_list'),
      
        path('', HomePageView.as_view(), name='home'),
]

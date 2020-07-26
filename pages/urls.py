from django.urls import path

from .views import HomePageView, TestsListView, TestDetailView, TestCreateView, TestDeleteView, TestUpdateView
from django.views.generic.base import TemplateView

urlpatterns = [
        path('test/<int:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),
        path('test/<int:pk>/edit/', TestUpdateView.as_view(), name='test_edit'),
        path('test/new', TestCreateView.as_view(), name='test_new'),
        path('test/<int:pk>', TestDetailView.as_view(), name='test_detail'),
        path('', HomePageView.as_view(), name='home'),
]

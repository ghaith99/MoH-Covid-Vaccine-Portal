import django_filters
from .models import Patient, Test
from crispy_forms.helper import FormHelper

class PatientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="First Name")
    last_name = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="Last Name")
    civil_ID = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="Civil ID")
    phone = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="Phone")
    city = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="City")
    nationality = django_filters.CharFilter(lookup_expr='icontains',distinct = True, label="Nationality")
    created_datetime = django_filters.DateFilter(label="Created Date")
    #date_range = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    class Meta:
        model = Patient
        fields = ['first_name']
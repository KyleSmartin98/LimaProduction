import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class DateInput(django_filters.FilterSet):
    input_type = 'date'

class SampleFilter(django_filters.FilterSet):
    logged_start_date = DateFilter(field_name="logged_date", lookup_expr='gte')
    logged_end_date = DateFilter(field_name="logged_date", lookup_expr='lte')
    expiration_start_date = DateFilter(field_name="expiration_date", lookup_expr='gte')
    expiration_end_date = DateFilter(field_name="expiration_date", lookup_expr='lte')
    tracking = CharFilter(field_name='tracking_number', lookup_expr='icontains')
    logged_by = CharFilter(field_name='logged_by', lookup_expr='icontains')
    description = CharFilter(field_name='sample_description', lookup_expr='icontains')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(SampleFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        sampletitles = ['logged_start_date', 'logged_end_date', 'expiration_start_date',
                        'expiration_end_date', 'logged_by', 'description']
        self.filters['tracking'].field.widget.attrs.update({
            'class': 'sample-searchbar',
            'placeholder': 'Tracking Number',
        })
        self.filters['tracking'].label = ''
        for i in sampletitles:
            self.filters[i].field.widget.attrs.update({
                'class': 'registration-input',
            })
            self.filters[i].label = ''



    class Meta:
        model = Sample
        fields = ['tracking_number', 'expiration_date', 'logged_date', 'logged_by', 'sample_description']



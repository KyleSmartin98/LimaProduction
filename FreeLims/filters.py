import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class DateInput(django_filters.FilterSet):
    input_type = 'date'

class SampleFilter(django_filters.FilterSet):
    name = CharFilter(field_name='sample_name', lookup_expr='icontains')
    logged_start_date = DateFilter(field_name="logged_date", lookup_expr='gte')
    logged_end_date = DateFilter(field_name="logged_date", lookup_expr='lte')
    expiration_start_date = DateFilter(field_name="expiration_date", lookup_expr='gte')
    expiration_end_date = DateFilter(field_name="expiration_date", lookup_expr='lte')
    tracking = CharFilter(field_name='tracking_number', lookup_expr='icontains')
    logged_by = CharFilter(field_name='logged_by', lookup_expr='icontains')
    description = CharFilter(field_name='sample_description', lookup_expr='icontains')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(SampleFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        sampletitles = ['name', 'logged_start_date', 'logged_end_date', 'expiration_start_date',
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
        fields = ['sample_name', 'tracking_number', 'expiration_date', 'logged_date', 'logged_by', 'sample_description']


class InventoryFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    manufacturer = CharFilter(field_name='manufacturer', lookup_expr='icontains')
    manufacturer_lot = CharFilter(field_name='manufacturer_lot', lookup_expr='icontains')
    lab_lot = CharFilter(field_name='Lab_lot', lookup_expr='icontains')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(InventoryFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        inventorytitles = ['name', 'manufacturer', 'manufacturer_lot', 'lab_lot']
        self.filters['name'].field.widget.attrs.update({
            'class': 'sample-searchbar',
            'placeholder': 'Reagent Name',
        })
        self.filters['manufacturer'].field.widget.attrs.update({
            'class': 'sample-searchbar',
            'placeholder': 'Vendor',
        })
        self.filters['manufacturer_lot'].field.widget.attrs.update({
            'class': 'sample-searchbar',
            'placeholder': 'Vendor Lot',
        })
        self.filters['lab_lot'].field.widget.attrs.update({
            'class': 'sample-searchbar',
            'placeholder': 'GlobaLIMS Lot',
        })
        for i in inventorytitles:
            self.filters[i].label = ''
    class Meta:
        model= Cheminventory
        fields = ['name', 'manufacturer', 'manufacturer_lot', 'Lab_lot']
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Sample, Cheminventory
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'type' : 'text',
            'placeholder' : 'Username',
            'class' : 'registration-input',
            'required' : '',
            'autocomplete': 'off',
        })
        self.fields["password1"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Password',
            'class': 'registration-input',
            'required': '',
            'autocomplete': 'off',
        })
        self.fields["password2"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Verify Password',
            'class': 'registration-input',
            'required': '',
            'autocomplete': 'off',
        })
        self.fields["organization"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Organization',
            'class': 'registration-input',
            'required': '',
            'autocomplete': 'off',
        })
        self.fields["email"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Email',
            'class': 'registration-input',
            'autocomplete': 'off',
        })

    organization = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=150, required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'organization', 'email']

class DateInput(forms.DateInput):
    input_type = 'date'

class SampleForm(ModelForm):
    sample_description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'registration-input-lg',
        'placeholder': 'Sample Description',

    }))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sampletitles = ['sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity',
                        'sample_type', 'expiration_date']
        self.fields["sample_name"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'sample-input',
            'autocomplete': 'off',
        })
        self.fields["tracking_number"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Tracking Number',
            'class': 'sample-input',
            'autocomplete': 'off',
        })
        self.fields["sample_volume"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Volume / Mass',
            'class': 'sample-input',
            'autocomplete': 'off',
        })
        self.fields["sample_quantity"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Quantity',
            'class': 'sample-input',
            'autocomplete': 'off',
        })
        self.fields["sample_type"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Type',
            'class': 'sample-input',
            'autocomplete': 'off',

        })
        self.fields["sample_type"].choices = [("", "Sample Type"), ] + list(
            self.fields["sample_type"].choices)[1:]
        self.fields["expiration_date"].widget.attrs.update({
            'type': 'date',
            'placeholder': 'Sample Expiration Date',
            'class': 'sample-input',
            'autocomplete': 'off',
            'style': 'font-family: Arial, sans-serif;'
        })

        for i in sampletitles:
            self.fields[i].label = ""



    expiration_date = forms.DateField(widget=DateInput)
    class Meta:
        model=Sample
        fields=['sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date']

class InitiateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initiatetitles = ['initiated','sample_test']
        self.fields["initiated"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Initiate?',
            'class': 'registration-input',
            'autocomplete': 'off',
            'style': 'margin-left: 70px'
        })
        self.fields["sample_test"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Test',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["sample_test"].choices = [("", "Sample Test"), ] + list(
            self.fields["sample_test"].choices)[1:]

        for i in initiatetitles:
            self.fields[i].label = ""

    class Meta:
        model=Sample
        fields=['initiated','sample_test']


class ResultForm(ModelForm):
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'registration-input-lg',
        'placeholder': 'Comment, if None: Write (N/A)',

    }))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resulttetitles = ['result_pf','sample_result','comments']
        self.fields["result_pf"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Passed?',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["sample_result"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Result',
            'class': 'registration-input',
            'autocomplete': 'off',
        })

        for i in resulttetitles:
            self.fields[i].label = ""

    class Meta:
        model = Sample
        fields = ['result_pf','sample_result','comments']

class InventoryForm(ModelForm):
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'reagent-input-lg',
        'placeholder': 'Comment, if None: Write (N/A)',
    }))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inventorytitles = ['name', 'manufacturer', 'manufacturer_lot', 'expiry', 'volume_size', 'location',
                           'comments']
        self.fields["name"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Reagent Name',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["manufacturer"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Vendor',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["manufacturer"].choices = [("", "Vendor"), ] + list(
            self.fields["manufacturer"].choices)[1:]
        self.fields["manufacturer_lot"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Vendor Lot Number',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["volume_size"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Volume | Mass',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["location"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Passed?',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["location"].choices = [("", "Storage Location"), ] + list(
            self.fields["location"].choices)[1:]
        self.fields["quarantine"].widget.attrs.update({
            'class': 'reagent-input',
            'style': 'margin-left:100px'
        })

        for i in inventorytitles:
            self.fields[i].label = ""

    expiry = forms.DateField(widget=DateInput(
        attrs={
            'class': 'reagent-input',
            'placeholder': 'Reagent Expiry',
            'style': 'margin-top:5px; '
                     'font-family: Arial, sans-serif;'
        }
    ))

    class Meta:
        model = Cheminventory
        fields = ['name', 'manufacturer', 'manufacturer_lot', 'expiry', 'volume_size', 'location', 'comments', 'quarantine']

class Qtyform(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Quantity',
            'class': 'reagent-input',
            'autocomplete': 'off',
        })
        self.fields["quantity"].label = ""

class DisposeForm(forms.Form):
    class Meta:
        model = Sample
        fields = ['inv_disposal']
class OpenForm(ModelForm):
    open_container = forms.BooleanField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["open_container"].widget.attrs.update({
            'type': 'text',
            'placeholder': '',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["open_container"].label = ""

    class Meta:
        model = Cheminventory
        fields = ['open_container']


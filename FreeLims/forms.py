from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Sample
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
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        """
        self.fields["sample_description"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Description',
            'class': 'registration-input-lg',
            'autocomplete': 'off',
        })
        """
        self.fields["tracking_number"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Tracking Number',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["sample_volume"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Volume / Mass',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["sample_quantity"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Quantity',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["sample_type"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Type',
            'class': 'registration-input',
            'autocomplete': 'off',
        })
        self.fields["expiration_date"].widget.attrs.update({
            'type': 'date',
            'placeholder': 'Sample Expiration Date',
            'class': 'registration-input',
            'autocomplete': 'off',
        })

        for i in sampletitles:
            self.fields[i].label = ""



    expiration_date = forms.DateField(widget=DateInput)
    class Meta:
        model=Sample
        fields=['sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date']



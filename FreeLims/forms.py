from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Sample
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'type' : 'text',
            'placeholder' : 'Username',
            'class' : 'registration-input',
            'required' : '',
        })
        self.fields["password1"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Password',
            'class': 'registration-input',
            'required': '',
        })
        self.fields["password2"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Verify Password',
            'class': 'registration-input',
            'required': '',
        })
        self.fields["organization"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Organization',
            'class': 'registration-input',
            'required': '',
        })
        self.fields["email"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Email',
            'class': 'registration-input',
        })

    organization = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=150, required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'organization', 'email']

class SampleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sample_name"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["sample_name"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["sample_name"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["sample_description"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["tracking_number"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["sample_quantity"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
        self.fields["expiration_date"].widget.attrs.update({
            'type': 'date',
            'placeholder': 'Sample Expiration Date',
            'class': 'registration-input',
        })
        self.fields["logged_by"].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Sample Name',
            'class': 'registration-input',
        })
    class Meta:
        model=Sample
        fields=['sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date', 'logged_by']



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Contact

class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name*', 'name': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone', 'class': 'form-control',}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message', 'rows': 4, 'class': 'form-control',}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control-file',}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?\d{10,12}$', phone):
            raise ValidationError('Invalid phone number format.')
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Avatar file size must not exceed 5MB.")
        return avatar

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
        })
    )
    country = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }, choices=[
            ('', 'Select your country'),
            ('Uzbekistan', 'Uzbekistan'),
            ('Russia', 'Russia'),
            ('USA', 'USA'),
            ('India', 'India'),
            ('London', 'London'),
        ])
    )
    street_address = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'House number and street name',
        })
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Town/City',
        })
    )
    state = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State/County',
        })
    )
    postcode = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Postcode/ZIP',
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
        })
    )


from django import forms

from .models import Account


class registrationform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter password',
        'class' : 'form-Control'
        }))
       
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
    
    def __init__(self, *args, **kwargs):
        super(registrationform, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastt Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
    def __init__(self, *args, **kwargs):
        super(VerifyForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['placeholder'] = 'Enter OTP'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
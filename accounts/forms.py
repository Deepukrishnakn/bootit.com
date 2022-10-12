
from dataclasses import field, fields
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
    def clean(self):
        cleaned_data=super(registrationform,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        phone_number=cleaned_data.get('phone_number')
        if len(phone_number) !=10:
            raise forms.ValidationError(
                'please enter valid phone number'
            )
        if len(password)<8:
            raise forms.ValidationError(
                'password must contain  atleast 8 characters'
            )
        if password !=confirm_password:
            raise forms.ValidationError(
                'password doesnot match...'
            )
        
        


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
    def __init__(self, *args, **kwargs):
        super(VerifyForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['placeholder'] = 'Enter OTP'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class userprofileform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name']
    def __init__(self, *args, **kwargs):
        super(userprofileform, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
        
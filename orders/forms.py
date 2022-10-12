from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'district', 'city', 'pincode']
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastt Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'address_line_1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'address_line_2'
        self.fields['country'].widget.attrs['placeholder'] = 'country'
        self.fields['state'].widget.attrs['placeholder'] = 'state'
        self.fields['district'].widget.attrs['placeholder'] = 'district'
        self.fields['city'].widget.attrs['placeholder'] = 'city'
        self.fields['pincode'].widget.attrs['placeholder'] = 'pincode'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    

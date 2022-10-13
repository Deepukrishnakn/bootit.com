from dataclasses import field, fields
from rest_framework import serializers
from vendor.models import Vendor



class VendorActivatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['is_active']
        


from store.models import Category,SubCategory,Product,Variation,Discount,ReviewRating,filter_price 
from django import forms
from orders.models import OrderProduct,Order
from accounts.models import Account

class categoryform(forms.ModelForm):
    class Meta:
        model= Category
        fields = '__all__'
        
class subcategoryform(forms.ModelForm):
    class Meta:
        model= SubCategory
        fields = '__all__'
        
class productform(forms.ModelForm):
    class Meta:
        model= Product
        fields =['product_name','description','price','slug','image','image1','image2','image3','stock','is_available','category','SubCategory']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['SubCategory'].queryset = SubCategory.objects.none()
        
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['SubCategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['SubCategory'].queryset = self.instance.category.subcategory_set.order_by('name')
            
        
class variationform(forms.ModelForm):
    class Meta:
        model= Variation
        fields = '__all__'
        
class orderproductform(forms.ModelForm):
    class Meta:
        model= OrderProduct
        fields =['order','payment','user','product','variations','quantity','product_price','ordered']
        
class usersform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter password',
        'class' : 'form-Control'
        }))
       
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))
    class Meta:
        model= Account
        fields =['first_name','last_name','username','email','phone_number','is_admin','is_staff','is_active','is_superadmin','password','confirm_password']
        
# class addadminform(forms.ModelForm):
#     class Meta:
#         model= Account
#         fields ='__all__'

class orderform(forms.ModelForm):
    class Meta:
        model= Order
        fields =['status']
    def __init__(self,*args, **kwargs):
        super(orderform,self).__init__(*args,**kwargs)
        self.fields['status'].widget.attrs.update({'class':'form-control'})
        
class couponform(forms.ModelForm):
    class Meta:
        model= Discount
        fields =['discount_code','discount_percentage','discount_from','is_active']
        
class reviewform(forms.ModelForm):
    class Meta:
        model= ReviewRating
        fields ='__all__'
        
        
class filterform(forms.ModelForm):
    class Meta:
        model= filter_price
        fields ='__all__'
        
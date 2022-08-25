from django import forms
from .models import User ,UserLicenseShipImage

class UserImageForm(forms.ModelForm):
  
    class Meta:
        model = User
        fields = ['phone','background_image', 'image']

class UserLicenseImageForm(forms.ModelForm):
  
    class Meta:
        model = UserLicenseShipImage
        fields = ['user', 'image','license']
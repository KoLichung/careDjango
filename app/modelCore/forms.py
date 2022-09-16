from django import forms
from .models import User ,UserLicenseShipImage, BlogPost ,AssistancePost

class UserBackGroundImageForm(forms.ModelForm):
  
    class Meta:
        model = User
        fields = ['phone','background_image']

class UserImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone', 'image']
class UserLicenseImageForm(forms.ModelForm):
  
    class Meta:
        model = UserLicenseShipImage
        fields = ['user', 'image','license']

class BlogPostCoverImageForm(forms.ModelForm):
  
    class Meta:
        model = BlogPost
        fields = ['id', 'body','cover_image']

class AssistancePostCoverImageForm(forms.ModelForm):
  
    class Meta:
        model = AssistancePost
        fields = ['id', 'body']
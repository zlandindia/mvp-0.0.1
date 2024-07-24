# eml_app/forms.py
from django import forms
from .models import UserDetail

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['name', 'age', 'mobile', 'gender', 'location', 'occupation', 'email']

class EmlUploadForm(forms.Form):
    eml_file = forms.FileField()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['feedback']

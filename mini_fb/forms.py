# File: mini_fb/forms.py
# Author: Veer Agrawal (veer1@bu.edu), 5/31/2025
# Description: Form for creating a new Profile.

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new Profile.
    """
    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'email', 'image_url']


class CreateStatusMessageForm(forms.ModelForm):
    """
    Form for creating a new Status Message for Profile
    """

    message = forms.CharField(label="Status Message", widget=forms.Textarea, required=True)

    class Meta:
        model = StatusMessage
        fields = ['message']
# File: views.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: Django views for the Mini Facebook app.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage

from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm



# Create your views here.

class ShowAllProfilesView (ListView):
    """defines a view class to show all profiles"""

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"



class ShowProfilePageView(DetailView):
    '''Show profile page for one user.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    """Handles the creation of a new Profile."""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class CreateStatusMessageView(CreateView):
    """
    View to create a new status message for a profile.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        """Add the profile to the context so the template can access it."""

        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Assign the profile to the status message before saving."""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the profile page after successful submission."""

        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
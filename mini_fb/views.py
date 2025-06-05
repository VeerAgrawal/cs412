# File: views.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: Django views for the Mini Facebook app.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image, StatusImage

from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm



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

        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            img = Image(profile=profile, image_file=file)
            img.save()

            link = StatusImage(image=img, status_message=sm)
            link.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the profile page after successful submission."""

        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    


class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

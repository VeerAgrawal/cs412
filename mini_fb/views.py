# File: views.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/10/2025  
# Description: Django views for the Mini Facebook app.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image, StatusImage

from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



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

    def get_context_data(self, **kwargs):
        """Add the user creation form to the context."""

        ctx = super().get_context_data(**kwargs)
        ctx['user_form'] = UserCreationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """
        Handle POST request by validating Django User form and the Profile form.
        If both valid, create the user, log them in, link the profile, and redirect.
        """
        user_form = UserCreationForm(request.POST)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid():
            # create new User
            user = user_form.save()
            # log them in
            login(request, user)
            # attach to Profile and save
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': profile_form, 'user_form': user_form})

    def get_success_url(self):
        """Redirect to created profile page."""

        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})

    

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """
    View to create a new status message for a profile.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    login_url = 'login'


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
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Allows user to update profile information."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    login_url = 'login'

    def get_success_url(self):
        """Redirect to the profile page"""
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """Handles deleting a specific status message."""

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'
    login_url = 'login'

    def get_success_url(self):
        """Redirect to the profile page"""

        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """Allows editing a previously posted status message."""
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    login_url = 'login'

    def get_success_url(self):
        """Redirect to the profile page"""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class AddFriendView(LoginRequiredMixin, View):
    """Adds a friendship between two profiles."""
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """Create new friend connection, then Redirect to profile page"""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other = Profile.objects.get(pk=self.kwargs['other_pk'])

        profile.add_friend(other)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """Displays friend suggestions for profile."""

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        """Add friend suggestions to template context"""

        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """Displays news feed of status messages from friends."""

    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    login_url = 'login'


    def get_context_data(self, **kwargs):
        """Add news feed to template context."""

        context = super().get_context_data(**kwargs)
        context['feed'] = self.object.get_news_feed()
        return context

# File: views.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: Django views for the Mini Facebook app.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


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

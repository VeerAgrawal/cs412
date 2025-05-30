# File: urls.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: URL patterns or the Mini Facebook app.

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),


]

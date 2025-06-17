# File: urls.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/15/2025  
# Description: URL patterns

from django.urls import path
from .views import VoterListView, VoterDetailView, VoterGraphView

urlpatterns = [
    # map the URL (empty string) to the view
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphView.as_view(), name='graphs'),

]
# File: urls.py
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025
# Description: URL patterns restaurant app.

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.home, name="home"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),

]

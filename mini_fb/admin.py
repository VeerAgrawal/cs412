# File: admin.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: Models show in the Django admin interface

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)

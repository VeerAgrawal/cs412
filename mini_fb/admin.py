# File: admin.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: Models show in the Django admin interface

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)

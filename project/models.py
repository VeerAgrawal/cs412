# File: models.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/20/2025  
# Description: Django models for an outfit tracking app

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class StyleTag(models.Model):
    """Represents a tag/ label used to classify outfit styles."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return name of the style tag."""

        return self.name

class Friend(models.Model):
    """Represents a Person/friend who the Outfit was worn with"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        """Return the friend's name."""
        return self.name

class addOutfit(models.Model):
    """Represents an outfit entry with a photo, date, and style tag."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='outfit_photos/')
    dateWorn = models.DateField()
    description = models.TextField(blank=True)
    styleTag = models.ForeignKey(StyleTag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """return string"""
        return f"{self.user.username} - {self.dateWorn}"
    

    def get_absolute_url(self):
        """Return URL of this outfit’s detail page (Mini-FB style)."""
        return reverse('outfit-detail', kwargs={'pk': self.pk})

class OutfitFriendLink(models.Model):
    """Links an outfit to a friend who was present"""
    
    outfit = models.ForeignKey(addOutfit, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

    def __str__(self):
        """return string"""
        return f"{self.outfit} with {self.friend}"



class Profile(models.Model):
    """
    Represents a user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='outfit_profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name  = models.CharField(max_length=30, blank=True)

    def __str__(self):
        """return string"""
        return f"{self.first_name} {self.last_name}".strip() or self.user.username
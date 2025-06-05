# File: models.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/31/2025  
# Description: This file defines Profile class and Status message class

from django.db import models
from django.utils import timezone

from django.urls import reverse


# Create your models here.
class Profile(models.Model):

    #define data atributes

    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.URLField(blank = True)

    def __str__(self):
        '''Return a string representation of this object.'''

    
        return f"{self.firstName} {self.lastName}"
    
    def get_absolute_url(self):
        """
        Returns the URL to display this profile's detail page.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        """Return all status messages for this profile, ordered by most recent"""

        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
class StatusMessage(models.Model):
    # Define a status message posted by a user

    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def get_images(self):
        """
        Returns all Image objects associated with this StatusMessage via StatusImage.
        """
        return Image.objects.filter(statusimage__status_message=self)


    def __str__(self):
        '''Return a string representation of this object.'''

        return f"{self.profile.firstName} - {self.message[:30]} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='mini_fb_images/')
    timestamp = models.DateTimeField(default=timezone.now)
    caption = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"{self.profile.firstName} - {self.caption or 'Image'}"

class StatusImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.image.id} for StatusMessage {self.status_message.id}"
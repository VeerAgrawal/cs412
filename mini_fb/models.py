# File: models.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/5/2025  
# Description: This file defines Profile class and Status message class

from django.db import models
from django.utils import timezone

from django.urls import reverse

from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):

    #define data atributes

    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.URLField(blank = True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    def get_friends(self):
        """
         Returns list of people that r friends with this profile.
        """
        friends = []

        # Friends where self is profile1
        f1 = Friend.objects.filter(profile1=self)
        friends += [f.profile2 for f in f1]

        # Friends where self is profile2
        f2 = Friend.objects.filter(profile2=self)
        friends += [f.profile1 for f in f2]

        return friends

    def add_friend(self, other):
        """
        Adds friendship between self and another Profile,
        if it doesn't already exist and isn't self-friending.
        """
        if self == other:
            return #so u cant friend yourself

        # Check if it already exists in either direction
        exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) |
            models.Q(profile1=other, profile2=self)
        ).exists()

        if not exists:
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        """
        Returns list of Profiles that are not already friends with u, and are not you.
        """
        all_profiles = Profile.objects.exclude(pk=self.pk)
        current_friends = self.get_friends()
        suggestions = all_profiles.exclude(pk__in=[f.pk for f in current_friends])
        return suggestions

    def get_news_feed(self):
        """
        Returns queryset of StatusMessages from you and all friends,
        """
        friends = self.get_friends()
        profiles = [self] + friends
        return StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')


    
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
    """Represents an image uploaded by a profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='mini_fb_images/')
    timestamp = models.DateTimeField(default=timezone.now)
    caption = models.CharField(max_length=240, blank=True)

    def __str__(self):
        """Return profile's name and image caption"""

        return f"{self.profile.firstName} - {self.caption or 'Image'}"

class StatusImage(models.Model):
    """links uploaded image with status message."""

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        """Return references to linked image and message."""
        return f"Image {self.image.id} for StatusMessage {self.status_message.id}"
    
class Friend(models.Model):
    """Friendship between two profiles."""
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string"""
        return f"{self.profile1.firstName} {self.profile1.lastName} & {self.profile2.firstName} {self.profile2.lastName}"

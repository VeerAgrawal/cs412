# File: models.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: This file defines Profile class with attributes such as name, city, email, and image URL.

from django.db import models

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
    
    
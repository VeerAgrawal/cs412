from django.contrib import admin

# Register your models here.

from .models import StyleTag, Friend, addOutfit, OutfitFriendLink

admin.site.register(StyleTag)
admin.site.register(Friend)
admin.site.register(addOutfit)
admin.site.register(OutfitFriendLink)

# File: forms.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/26/2025  
# Description: Django form classes for the Outfit Tracker app. Includes forms for 
# creating profiles, outfits (with friends and tags), friend management, and analytics filters.

from django import forms
from .models import Profile, addOutfit, Friend, OutfitFriendLink, StyleTag

class CreateProfileForm(forms.ModelForm):
    """Form to create a new user profile (first and last name)."""

    class Meta:
        model  = Profile
        fields = ['first_name', 'last_name']

class OutfitForm(forms.ModelForm):
    """Form to add or edit an outfit with photo, friends, tags, and description."""

    dateWorn = forms.DateField(widget=forms.SelectDateWidget())
    
    friends = forms.ModelMultipleChoiceField(
        queryset=Friend.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    new_friends = forms.CharField(
        label="Add new friends (comma-separated)",
        required=False
    )


    class Meta:
        model  = addOutfit
        fields = ['photo', 'dateWorn', 'description', 'styleTag', 'friends', 'new_friends']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}), 
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with user context"""

        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # limit friend list to this user
        self.fields['friends'].queryset = Friend.objects.filter(user=user)

        # when editing, pre-select already–linked friends
        if self.instance.pk:
            current = Friend.objects.filter(outfitfriendlink__outfit=self.instance)
            self.initial['friends'] = current

        self._user = user

    def save(self, commit=True, user=None):
        """Save Outfit, update links, create any new friends entered."""
        outfit = super().save(commit=False)

        if user and not outfit.pk:
            outfit.user = user
        if commit:
            outfit.save()

        selected = list(self.cleaned_data.get('friends'))
        # remove links that were unchecked
        OutfitFriendLink.objects.filter(outfit=outfit).exclude(friend__in=selected).delete()
        # add missing links for checked friends
        for f in selected:
            OutfitFriendLink.objects.get_or_create(outfit=outfit, friend=f)

        # new friends typed in 
        names = self.cleaned_data.get('new_friends', '')
        if names:
            for name in [n.strip() for n in names.split(',') if n.strip()]:
                friend, _ = Friend.objects.get_or_create(user=self._user, name=name)
                OutfitFriendLink.objects.get_or_create(outfit=outfit, friend=friend)

        return outfit


class FriendForm(forms.ModelForm):
    """Create / edit a Friend (name + notes)."""
    class Meta:
        model  = Friend
        fields = ['name', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 1}), 
        }



class OutfitFilterForm(forms.Form):
    """Form to filter outfits by date, style, and friends."""

    friends   = forms.ModelMultipleChoiceField(
        queryset=Friend.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Friends"
    )
    style_tag = forms.ModelChoiceField(
        queryset=StyleTag.objects.all(),
        required=False,
        empty_label="(Any style)",
        label="Style"
    )
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to   = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    date_exact = forms.DateField(
        label="Specific Date",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        """Restrict friend choices to those belonging to the logged in user"""

        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # limit friend list to this user
        self.fields['friends'].queryset = Friend.objects.filter(user=user)


class StyleAnalyticsForm(forms.Form):
    """Form to filter style analytics charts by date range."""

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="From"
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="To"
    )

# File: views.py
# Author: Veer Agrawal (veer1@bu.edu), 6/25/2025
# Description: Django views for the personal outfit tracker app.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from .models import addOutfit, OutfitFriendLink, Friend
from .forms import CreateProfileForm, OutfitForm, FriendForm, Friend, OutfitFilterForm, StyleAnalyticsForm

import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo


# Sign up new user and log them in
class CreateProfileView(CreateView):
    """Create a new User and a linked Profile in one step."""
    template_name = 'project/signup.html'  
    form_class    = CreateProfileForm            

    def get_context_data(self, **kwargs):
        """add the UserCreationForm to the context"""
        ctx = super().get_context_data(**kwargs)
        ctx['user_form'] = UserCreationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        '''handle both forms together'''
        user_form = UserCreationForm(request.POST)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            login(request, user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('outfit-list')
        else:
            return render(request, self.template_name, {'form': profile_form, 'user_form': user_form})


class MainView(TemplateView):
    """Render the main homepage template"""
    template_name = 'project/main.html'


class OutfitListView(LoginRequiredMixin, ListView):
    """List all outfits for the logged-in user"""
    model               = addOutfit
    template_name       = 'project/outfit_list.html'
    context_object_name = 'outfits'
    login_url           = 'login'

    def get_queryset(self):
        """ Return outfits filtered by selected friends, style tags, and date range. """
        qs = addOutfit.objects.filter(user=self.request.user)

        # build filters
        friends   = self.request.GET.getlist('friends')
        style_tag = self.request.GET.get('style_tag')
        date_from = self.request.GET.get('date_from')
        date_to   = self.request.GET.get('date_to')
        date_exact  = self.request.GET.get('date_exact')

        if friends:
            qs = qs.filter(outfitfriendlink__friend__id__in=friends).distinct()
        if style_tag:
            qs = qs.filter(styleTag__id=style_tag)
        if date_exact:
            qs = qs.filter(dateWorn=date_exact)
        else: 
            if date_from:
                qs = qs.filter(dateWorn__gte=date_from)
            if date_to:
                qs = qs.filter(dateWorn__lte=date_to)

        return qs.order_by('-dateWorn')

    def get_context_data(self, **kwargs):
        """ Add the outfit filter form to the template context """
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = OutfitFilterForm(self.request.GET or None, user=self.request.user)
        return ctx
    

class OutfitDetailView(LoginRequiredMixin, DetailView):
    """Show details for one outfit"""
    model = addOutfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        """add context date for template"""
        context = super().get_context_data(**kwargs)
        context['friends'] = OutfitFriendLink.objects.filter(outfit=self.object)
        return context


class OutfitCreateView(LoginRequiredMixin, CreateView):
    """Create a new outfit"""
    model = addOutfit
    form_class = OutfitForm
    template_name = 'project/outfit_form.html'
    login_url = 'login'
    
    def get_form_kwargs(self):
        """
        Pass the logged-in user to the form to filter friends list.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user    
        return kwargs
    
    def form_valid(self, form):
        """
        Save the outfit with the associated user and redirect to detail view.
        """
        form.save(user=self.request.user)
        return redirect('outfit-detail', pk=form.instance.pk)

class OutfitUpdateView(LoginRequiredMixin, UpdateView):
    """Allow the user to update one of their outfits."""

    model = addOutfit
    form_class = OutfitForm
    template_name = 'project/outfit_form.html'
    login_url = 'login'
    
    def get_queryset(self):
        """
        Restrict queryset to outfits owned by the logged-in user.
        """
        return addOutfit.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        """
        Pass the logged-in user to the form to limit friend options.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """
        Save the updated outfit and redirect to its detail page.
        """
        form.save(user=self.request.user)
        return redirect('outfit-detail', pk=form.instance.pk)


class OutfitDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an outfit"""
    model = addOutfit
    template_name = 'project/outfit_confirm_delete.html'
    success_url = reverse_lazy('outfit-list')
    login_url = 'login'

    def get_queryset(self):
        """queryset"""
        return addOutfit.objects.filter(user=self.request.user)



class FriendListView(LoginRequiredMixin, ListView):
    """Show all friends for the logged-in user."""
    model = Friend
    template_name = 'project/friend_list.html'
    context_object_name = 'friends'
    login_url = 'login'

    def get_queryset(self):
        """queryset"""
        return Friend.objects.filter(user=self.request.user)


class FriendDetailView(LoginRequiredMixin, DetailView):
    """Show one friend (name + notes)."""
    model = Friend
    template_name = 'project/friend_detail.html'
    context_object_name = 'friend'
    login_url = 'login'

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)


class FriendCreateView(LoginRequiredMixin, CreateView):
    """create friend view"""
    model = Friend
    form_class = FriendForm
    template_name = 'project/friend_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('friend-list')

class FriendUpdateView(LoginRequiredMixin, UpdateView):
    """Allow the user to edit one of their friends."""
    model = Friend
    form_class = FriendForm
    template_name = 'project/friend_form.html'
    login_url = 'login'

    def get_queryset(self):
        """queryset"""
        return Friend.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Redirect to the friend list after a successful update"""
        return reverse('friend-list')

class FriendDeleteView(LoginRequiredMixin, DeleteView):
    """Allow the user to delete one of their friends."""
    model = Friend
    template_name = 'project/friend_confirm_delete.html'
    success_url = reverse_lazy('friend-list')
    login_url = 'login'

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)
    

class AnalyticsView(LoginRequiredMixin, TemplateView):
    """Display a pie chart summarizing style tag usage over time."""
    template_name = 'project/analytics.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        """
        Generate analytics data based on filtered outfits.
        Includes a pie chart of style tag frequencies.
        """
        ctx  = super().get_context_data(**kwargs)
        form = StyleAnalyticsForm(self.request.GET or None)
        ctx['form'] = form

    
        qs = addOutfit.objects.filter(user=self.request.user)
        if form.is_valid():
            if form.cleaned_data.get('date_from'):
                qs = qs.filter(dateWorn__gte=form.cleaned_data['date_from'])
            if form.cleaned_data.get('date_to'):
                qs = qs.filter(dateWorn__lte=form.cleaned_data['date_to'])

        
        df = pd.DataFrame(list(qs.values('styleTag__name')))

        if not df.empty:
            # Count occurrences of each style tag
            counts = df['styleTag__name'].value_counts(dropna=False)
            labels = [label or "Un-tagged" for label in counts.index]
            values = counts.values

            fig = go.Figure(
                data=[go.Pie(labels=labels, values=values, textinfo='label+percent')],
                layout_title_text="Style Tags Worn"
            )

            ctx['graph_div'] = pyo.plot(fig, output_type='div', include_plotlyjs=False)
        else:
            ctx['graph_div'] = None

        return ctx

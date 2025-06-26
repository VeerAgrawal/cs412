# File: urls.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/25/2025  
# Description: URL patterns for the Outfit Tracker app.

from django.urls import path
from .views import (OutfitListView, OutfitDetailView, OutfitCreateView,
                    OutfitUpdateView, OutfitDeleteView, CreateProfileView,
                    FriendListView, FriendDetailView, FriendCreateView, 
                    FriendUpdateView, FriendDeleteView, MainView, AnalyticsView )
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(MainView.as_view(), login_url='login'), name='main'),
    path('outfits/', login_required(OutfitListView.as_view(), login_url='login'), name='outfit-list'),
    path('outfit/<int:pk>/', login_required(OutfitDetailView.as_view(), login_url='login'), name='outfit-detail'),
    path('outfit/create/', login_required(OutfitCreateView.as_view(), login_url='login'), name='outfit-create'),
    path('outfit/<int:pk>/update/', login_required(OutfitUpdateView.as_view(), login_url='login'), name='outfit-update'),
    path('outfit/<int:pk>/delete/', login_required(OutfitDeleteView.as_view(), login_url='login'), name='outfit-delete'),
    path('signup/', CreateProfileView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('friends/', login_required(FriendListView.as_view(), login_url='login'), name='friend-list'),
    path('friends/add/', login_required(FriendCreateView.as_view(),login_url='login'), name='friend-add'),
    path('friends/<int:pk>/', login_required(FriendDetailView.as_view(), login_url='login'), name='friend-detail'),
    path('friends/<int:pk>/edit/', login_required(FriendUpdateView.as_view(), login_url='login'), name='friend-edit'),
    path('friends/<int:pk>/delete/', login_required(FriendDeleteView.as_view(),login_url='login'), name='friend-delete'),
    path('analytics/', login_required(AnalyticsView.as_view(), login_url='login'), name='analytics'),
]

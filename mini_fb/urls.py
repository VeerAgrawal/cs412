# File: urls.py  
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025  
# Description: URL patterns or the Mini Facebook app.

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView
from .views import CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView
from .views import UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView
from .views import ShowNewsFeedView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', login_required(CreateStatusMessageView.as_view(), login_url='login'), name="create_status"),
    path('profile/<int:pk>/update', login_required(UpdateProfileView.as_view(), login_url='login'), name='update_profile'),
    path('status/<int:pk>/delete', login_required(DeleteStatusMessageView.as_view(), login_url='login'), name='delete_status'),
    path('status/<int:pk>/update', login_required(UpdateStatusMessageView.as_view(), login_url='login'), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', login_required(AddFriendView.as_view(), login_url='login'), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions', login_required(ShowFriendSuggestionsView.as_view(), login_url='login'), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed', login_required(ShowNewsFeedView.as_view(), login_url='login'), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

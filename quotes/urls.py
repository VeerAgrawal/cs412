from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    
    path(r'', views.home, name="home_page"),
    path(r'about', views.about, name="about_page"),
    path(r'quote', views.home, name="quote_page"),
    path(r'showall', views.showall, name="showall_page"),

]
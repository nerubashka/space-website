"""
Definition of urls for SpaceWebsite.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import include


urlpatterns = [
    path('', views.home, name='home'),
    path('news', views.news, name='news'),
    path('events/list/', views.event_list),
    path('events/<int:event_id>/', views.event_list_id),
    path('admin/', admin.site.urls),
    path('djrichtextfield/', include('djrichtextfield.urls'))
]

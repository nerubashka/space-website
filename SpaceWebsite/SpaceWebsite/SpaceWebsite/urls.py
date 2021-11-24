"""
Definition of urls for SpaceWebsite.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('news', views.NewsListView.as_view(), name='news'),
    path('about', views.about, name='about'),
    path('events/list/', views.event_list),
    path('events/<int:event_id>/', views.event_list_id),
    path('admin/', admin.site.urls),
    path('djrichtextfield/', include('djrichtextfield.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

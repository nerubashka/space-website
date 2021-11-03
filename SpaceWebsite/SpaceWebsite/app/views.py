"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from .models import Event
import json


def event_list(request):
    """Return JSON for all events"""
    e = Event.objects.all()
    return HttpResponse([x.tojson() for x in list(e)])


def event_list_id(request, event_id):
    """Return JSON for event by id"""
    e = Event.objects.get(pk=event_id)
    return HttpResponse(e.tojson())


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )

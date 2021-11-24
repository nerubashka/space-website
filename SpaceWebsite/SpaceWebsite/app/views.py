"""
Definition of views.
"""
# -*- coding: utf-8 -*-


from datetime import datetime

from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Event, News, CommonText

def get_event_list(request, **kwargs):
    events = Event.objects.all()
    title = request.GET.get('title')
    sort_up = request.GET.get('sort_up')
    sort_down = request.GET.get('sort_down')
    date = request.GET.get('date')
    text = request.GET.get('text')
    uptodate = request.GET.get('uptodate')

    if title is not None:
        events = events.filter(title__iexact=title)
    if date is not None:
        events = events.filter(begin_date__iexact=date)
    if uptodate:
        events = events.filter(end_data__gte = datetime.now())
    if text is not None:
        events = events.filter(description__contains=text)
    if sort_up:
        events = events.order_by('-begin_date')
    if sort_down:
        events = events.order_by('begin_date')

    return events

def event_list(request, **kwargs):
    """Return JSON for all events with search and sorting"""
    events = get_event_list(request, **kwargs)
    return HttpResponse([x.tojson() for x in list(events)])



def event_list_id(request, event_id):
    """Return JSON for event by id"""
    e = Event.objects.get(pk=event_id)
    return HttpResponse(e.tojson())



def new_list(request, **kwargs):
    """Return JSON for all events with search and sorting"""
    s = request.GET.get('offset')
    e = request.GET.get('limit')
    news = News.objects.all().filter(publishing_date__lte = datetime.now()).order_by('-publishing_date')[s:e]
    return HttpResponse(news)


def news(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    t = CommonText.objects.all().filter(title='Новости')
    events = get_event_list(request)
    events = events.filter(end_data__gte = datetime.now()).order_by('begin_date')[:5]
    for e in events:
        if e.begin_date < e.end_data:
            e.long = True
        else:
            e.long = False
    
    news = News.objects.all().filter(publishing_date__lte = datetime.now()).order_by('-publishing_date')[:1]        
            
    g_str = " "
    if len(t) > 0:
        g_str = t[0].text
    return render(
        request,
        'app/news.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'page_name': 'news',
            'greetings': g_str,
            'events': events,
            'news': news,
            'sub_page': 'news',
        }
    )


class NewsListView(ListView):
    model = News
    template_name = 'app/news.html'
    page_name = 'news'
    events =  Event.objects.all().filter(end_data__gte = datetime.now()).order_by('begin_date')[:5]
    sub_page = 'news'
    paginate_by = 5
    

    def get_context_data(self, **kwargs):
        for e in self.events:
            if e.begin_date < e.end_data:
                e.long = True
            else:
                e.long = False
    
        # Call the base implementation first to get the context
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['page_name'] = self.page_name
        context['sub_page'] = self.sub_page
        context['events'] = self.events
        return context

def home(request):
    return news(request)

def about(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    t = CommonText.objects.all().filter(title='О нас')
    g_str = " "
    if len(t) > 0:
        g_str = t[0].text
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'page_name': 'about',
            'greetings': g_str,
            'sub_page': 'news',
        }
    )



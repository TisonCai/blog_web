from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Link
from blog.views import CommonViewMixin

class LinkListView(ListView,CommonViewMixin):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

# Create your views here.
def links(request):
    return HttpResponse('links')
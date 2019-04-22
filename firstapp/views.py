from django.shortcuts import render, HttpResponse
from firstapp.models import Apartment_list
from django.template import Context, Template

# Create your views here.
def apartment(request):
    queryset1 = request.GET.get('city')
    if queryset1:
        apartment_list = Apartment_list.objects.filter(city = queryset1)
    else:
        apartment_list = Apartment_list.objects.all()
    context = {}
    context['apartment_list'] = apartment_list
    index_page = render(request, 'apartment.html', context)
    return index_page

def apartment_detail(request):
    context = {}
    return  render(request, 'apartment_detail.html', context)
def apartment_details(request):
    context = {}
    return  render(request, 'apartment_details.html', context)

def homepage(request):
    context = {}
    return  render(request, 'Homepage.html', context)

def list(request):
    context = {}
    return  render(request, 'List.html', context)

def lists(request):
    context = {}
    return  render(request, 'Lists.html', context)

def login(request):
    context = {}
    return  render(request, 'register_login.html', context)

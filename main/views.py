from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def register_page(request):
    template = loader.get_template('main/register.html')
    languages = Language.objects.order_by('language_name')
    universities = University.objects.order_by('university_name')
    competition = Competition.objects.all()
    context = {
        'languages': languages,
        'universities': universities,
        'competition': competition,
        'msg':'salam'
    }
    return HttpResponse(template.render(context, request))



def login(request):
    context = {}
    print('salam',request.POST)
    if request.META.get('HTTP_REFERER').split('/')[-1] == 'register':
        context['message'] = 'OK'
        print('ahsnat ')
    template = loader.get_template('main/login.html')
    return HttpResponse(template.render(context, request))

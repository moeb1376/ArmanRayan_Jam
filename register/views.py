from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from main.models import *


# Create your views here.

def team_register(request):
    template = loader.get_template('register/register.html')
    languages = Language.objects.order_by('language_name')
    universities = University.objects.order_by('university_name')
    competition = Competition.objects.all()
    print('******', languages[0])
    contex = {
        'a': 'salam',
        'languages': languages,
        'universities':universities,
        'competition':competition
    }
    return HttpResponse(template.render(contex, request))

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.urls import resolve
from main.models import *
from .models import *

register_failed = False
register_context = {}


# Create your views here.

def register_page(request):
    context = {
        'team_name': '',
        'f_name': '',
        'l_name': '',
        'email': '',
        'password': '',
        'my_messages': []
    }
    if request.META.get('HTTP_REFERER').split('/')[-1] == 'register':
        t = list(Team.objects.filter(team_name=request.POST['team_name']))
        e = list(User.objects.filter(email=request.POST['email']))
        if len(t) == 0 and len(e) == 0:
            team = Team()
            user = User()
            university = University.objects.get(pk=int(request.POST['university'][0]))
            languages = Language.objects.get(pk=int(request.POST['lang'][0]))
            competition = Competition.objects.get(pk=int(request.POST['leagues'][0]))
            team.create_by_form(request.POST, competition, university, languages)
            team.save()
            user.create_by_form(request.POST, team, university, True)
            user.save()
            messages.success(request, 'ثبت نام با موفقیت انجام شد')
            return HttpResponseRedirect('/login')
        else:
            if len(t) > 0:
                context['my_messages'].append('نام تیم تکراری است')
                context['team_name_color'] = True
            if len(e) > 0:
                context['my_messages'].append('کاربری دیگر با این ایمیل ثبت شده است')
                context['email_color'] = True
            keys = context.keys()
            for i in request.POST:
                if i in keys:
                    context[i] = request.POST[i]
    template = loader.get_template('register/register.html')
    languages = Language.objects.order_by('language_name')
    universities = University.objects.order_by('university_name')
    competition = Competition.objects.all()
    print('******', languages[0])
    context.update({
        'languages': languages,
        'universities': universities,
        'competition': competition
    })
    return HttpResponse(template.render(context, request))


def login(request):
    # global register_context
    # global register_failed
    # context = {}
    # print('salam', request.POST)
    if request.META.get('HTTP_REFERER','').split('/')[-1] == 'login':
        print(request.GET)
        team = list(Team.objects.filter(team_name=request.GET['team_name']))
        if len(team) > 0:
            if team[0].password == request.GET['password'][0]:
                messages.success(request, 'ورود موفقیت آمیز')
                return HttpResponseRedirect('/jam')
            else:
                messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
        else:
            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
    template = loader.get_template('register/login.html')
    return HttpResponse(template.render({}, request))

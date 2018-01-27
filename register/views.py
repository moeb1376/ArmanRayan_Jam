from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.urls import resolve
from main.models import *
from .models import *

register_failed = False
register_context = {}


# Create your views here.

def register_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/jaam')
    context = {
        'team_name': '',
        'f_name': '',
        'l_name': '',
        'email': '',
        'password': '',
        'my_messages': []
    }
    print('int register page request post:', request.POST)
    if request.META.get('HTTP_REFERER').split('/')[-1] == 'register':
        t = list(auth_user.objects.filter(username=request.POST['team_name']))
        e = list(User.objects.filter(email=request.POST['email']))
        if len(t) == 0 and len(e) == 0:
            team = Team()
            # user = User()
            university = University.objects.get(pk=int(request.POST['university'][0]))
            languages = Language.objects.get(pk=int(request.POST['lang'][0]))
            competition = Competition.objects.get(pk=int(request.POST['leagues'][0]))
            team.create_by_form(request.POST, competition, university, languages)
            team.save()
            # user.create_by_form(request.POST, team, university, True)
            # user.save()
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


def login_page(request):
    http_referer = request.META.get('HTTP_REFERER', '').split('/')[-1]
    if request.user.is_authenticated:
        print('revalle')
        return HttpResponseRedirect('/jaam')
        # logout(request)
    else:
        print(list(messages.get_messages(request)))
        print("reval nist")

    if http_referer == 'login':
        username = request.POST['username']
        password = request.POST['password']
        temp_user = authenticate(username=username, password=password)
        print(temp_user)
        if temp_user is not None:
            login(request, temp_user)
            # messages.success(request, 'ورود موفقیت آمیز')
            return HttpResponseRedirect('/jaam')
        else:
            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
    template = loader.get_template('register/login.html')
    return HttpResponse(template.render({}, request))

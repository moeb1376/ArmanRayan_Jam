import requests
from builtins import len
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from validate_email import validate_email

from main.models import *
from .models import *
from .forms import UserRegisterForm, TeamForm, UserLoginForm
from Jam.settings import GOOGLE_RECAPTCHA_SECRET_KEY

register_failed = False
register_context = {}


# Create your views here.

def register_page(request):
    print(type(request.user))
    if request.user.is_authenticated and not request.user.is_superuser:
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
        'competition': competition,
        'user_form': UserForm(),
        'team_form': TeamForm(),

    })
    return HttpResponse(template.render(context, request))


def register_page2(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect('/jaam')
    print('request register page : ', request)
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        user_form = UserRegisterForm(request.POST)
        team_form.changed_required_mentor()
        user_form.changed_password_label()
        if user_form.is_valid() and team_form.is_valid():
            # ''' Begin reCAPTCHA validation '''
            # recaptcha_response = request.POST.get('g-recaptcha-response')
            # data = {
            #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
            #     'response': recaptcha_response
            # }
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            # result = r.json()
            # ''' End reCAPTCHA validation '''
            email_objects = auth_user.objects.filter(email=user_form.cleaned_data['email'])
            print('WTemail: ', email_objects, user_form.cleaned_data['email'])
            check_email = False
            for e in email_objects:
                if not e.is_superuser:
                    check_email = True
            if check_email:
                user_form.add_error('email', 'ایمیل تکراری است')
            # if result['success'] and not check_email:
            if not check_email:
                temp = user_form.save()
                team = team_form.save(commit=False)
                team.user_team = temp
                team.save()
                return HttpResponseRedirect('/login')
    else:
        user_form = UserRegisterForm()
        team_form = TeamForm()
    user_form.changed_password_label()
    team_form.changed_required_mentor()
    template = loader.get_template('register/register.html')
    context = {
        'user_form': user_form,
        'team_form': team_form,
    }
    return HttpResponse(template.render(context, request))


def login_page(request):
    http_referer = request.META.get('HTTP_REFERER', '').split('/')[-1]
    print(request.user.is_superuser)
    if request.user.is_authenticated and not request.user.is_superuser:
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


def login_page2(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        print('revalle')
        return HttpResponseRedirect('/jaam')
    if request.method == "POST":
#        print(request)
        auth_form = UserLoginForm(request.POST)
        print('auth_form is valid ', auth_form.is_valid())
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            email_login = validate_email(username)
            print('username : %s password : %s email_login ' % (username, password), email_login)
            if email_login:
                try:
                    temp_user = auth_user.objects.get(email=username)
                    if temp_user.check_password(password):
                        login(request, temp_user)
                        print("user team set len ", len(temp_user.Teams.all()[0].Users.all()))
                        if len(temp_user.Teams.all()[0].Users.all()) < 2:
                            return HttpResponseRedirect('/setting')
                        return HttpResponseRedirect('/jaam')
                except auth_user.DoesNotExist:
                    auth_form.add_error('username', 'نام کاربری یا رمز عبور اشتباه است')
            else:
                temp_user = authenticate(username=username, password=password)
                if temp_user is not None and not temp_user.is_superuser:
                    login(request, temp_user)
                    return HttpResponseRedirect('/jaam')
                else:
                    auth_form.add_error('username', 'نام کاربری یا رمز عبور اشتباه است')
    else:
        auth_form = UserLoginForm()
    template = loader.get_template('register/login.html')
    return HttpResponse(template.render({'auth_form': auth_form}, request))

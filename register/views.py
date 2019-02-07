from builtins import len
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from validate_email import validate_email
from .models import *
from .forms import UserRegisterForm, TeamForm, UserLoginForm
from main.models import Mentor
from SPC_main.views import SPC_main_page

register_failed = False
register_context = {}


def old_register_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect("SPC_main:SPC_main_page")
    print('request register page : ', request)
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        user_form = UserRegisterForm(request.POST)
        team_form.changed_required_mentor()
        user_form.changed_password_label()
        team_form.change_empty_label()
        if user_form.is_valid() and team_form.is_valid():
            email_objects = auth_user.objects.filter(email=user_form.cleaned_data['email'])
            mentor_objects = Mentor.objects.filter(code=team_form.cleaned_data['mentor'])
            print('WTemail: ', email_objects, user_form.cleaned_data['email'])
            check_email = False
            check_mentor = False
            for e in email_objects:
                if not e.is_superuser:
                    check_email = True
            if len(mentor_objects) == 0 and team_form.cleaned_data['mentor'] != '':
                check_mentor = True
            if check_email:
                user_form.add_error('email', 'ایمیل تکراری است')
            if check_mentor:
                team_form.add_error('mentor', 'کد منتور صحیح نمی‌باشد')
                team_form.add_error(None, 'کد منتور صحیح نمی‌باشد')
            if not (check_email or check_mentor):
                temp = user_form.save()
                team = team_form.save(commit=False)
                team.user_team = temp
                team.save()
                return redirect("register:login")
    else:
        user_form = UserRegisterForm()
        team_form = TeamForm()
    user_form.changed_password_label()
    team_form.changed_required_mentor()
    team_form.change_empty_label()
    template = loader.get_template('Old/register.html')
    context = {
        'user_form': user_form,
        'team_form': team_form,
    }
    return HttpResponse(template.render(context, request))


def old_login_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        print('revalle')
        return redirect('SPC_main:SPC_main_page')
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
                print(temp_user)
                if temp_user is not None and not temp_user.is_superuser:
                    login(request, temp_user)
                    return HttpResponseRedirect('/jaam')
                else:
                    auth_form.add_error('username', 'نام کاربری یا رمز عبور اشتباه است')
    else:
        auth_form = UserLoginForm()
    template = loader.get_template('Old/login.html')
    return HttpResponse(template.render({'auth_form': auth_form}, request))


def login_page(request):
    valid_option = {
        "username": "validate ",
        "password": "validate "
    }
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('SPC_main:SPC_main_page')
    if request.method == "POST":
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
                        if len(temp_user.Teams.all()[0].Users.all()) < 2:
                            return redirect('setting:setting')
                        return redirect('SPC_main:SPC_main_page')
                except auth_user.DoesNotExist:
                    auth_form.add_error('username', 'نام کاربری یا رمز عبور اشتباه است')
                    valid_option['username'] += "invalid"
            else:
                temp_user = authenticate(username=username, password=password)
                print(temp_user)
                if temp_user is not None and not temp_user.is_superuser:
                    login(request, temp_user)
                    return redirect("SPC_main:SPC_main_page")
                else:
                    auth_form.add_error('username', 'نام کاربری یا رمز عبور اشتباه است')
                    valid_option['username'] += "invalid"
    else:
        auth_form = UserLoginForm()

    context = {
        'auth_form': auth_form,
        "validate": valid_option
    }
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def register_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect("SPC_main:SPC_main_page")
    print('request register page : ', request)
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        user_form = UserRegisterForm(request.POST)
        team_form.changed_required_mentor()
        user_form.changed_password_label()
        team_form.change_empty_label()
        if user_form.is_valid() and team_form.is_valid():
            email_objects = auth_user.objects.filter(email=user_form.cleaned_data['email'])
            # mentor_objects = Mentor.objects.filter(code=team_form.cleaned_data['mentor'])
            print('WTemail: ', email_objects, user_form.cleaned_data['email'])
            check_email = False
            check_mentor = False
            for e in email_objects:
                if not e.is_superuser:
                    check_email = True
            # if len(mentor_objects) == 0 and team_form.cleaned_data['mentor'] != '':
            #     check_mentor = True
            if check_email:
                user_form.add_error('email', 'ایمیل تکراری است')
            if check_mentor:
                team_form.add_error('mentor', 'کد منتور صحیح نمی‌باشد')
                team_form.add_error(None, 'کد منتور صحیح نمی‌باشد')
            if not (check_email or check_mentor):
                temp = user_form.save()
                team = team_form.save(commit=False)
                team.user_team = temp
                team.save()
                return redirect("register:login")
    else:
        user_form = UserRegisterForm()
        team_form = TeamForm()
    user_form.changed_password_label()
    team_form.changed_required_mentor()
    team_form.change_empty_label()
    template = loader.get_template('signup.html')
    context = {
        'user_form': user_form,
        'team_form': team_form,
    }
    return HttpResponse(template.render(context, request))

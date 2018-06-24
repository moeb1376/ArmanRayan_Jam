from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, loader, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from register.models import Team
from .models import Cup


# Create your views here

@login_required(login_url='/login', redirect_field_name='')
def SPC_main_page(request):
    print(request.META.get("upload_code", 0))
    print(request.user)
    team = request.user.Teams.all()[0]
    team_member = team.Users.all()
    user_require = 2 if team.competition.competition_level < 3 else 1
    print(user_require, team.competition.competition_level)
    if len(team_member) < user_require:
        return HttpResponseRedirect('/setting')
    for member in team_member:
        print(member.user_lname)
    context = {
        'team': team,
        'members': team_member
    }
    if team.competition.competition_level < 3:
        print('jaam2')
        template = loader.get_template('SPC_main/jaam2.html')
    else:
        print('jaamiac')
        template = loader.get_template('SPC_main/jaam_iac.html')
    return HttpResponse(template.render(context, request))


def team_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login', redirect_field_name='')
def table_view(request):
    send_mail('test', 'havij salam', settings.EMAIL_HOST_USER, ['m_mohammadaliebrahim@comp.iust.ac.ir'])
    login_team = request.user.Teams.all()[0]
    if login_team.competition.competition_level < 3:
        print('jaam2')
        teams = Team.objects.filter(competition=login_team.competition)
        template = loader.get_template('SPC_main/table-spc.html')
    else:
        print('jaamiac')
        template = loader.get_template('SPC_main/table_iac.html')
        teams = dict()
        teams['picture'] = Team.objects.filter(competition__competition_level=5)
        teams['sound'] = Team.objects.filter(competition__competition_level=4)
        teams['text'] = Team.objects.filter(competition__competition_level=3)
    context = {
        'login_team': login_team,
        'teams': teams
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login', redirect_field_name='')
def cup_view(request):
    if request.method == 'GET':
        print('GET')
        login_team = request.user.Teams.all()[0]
        teams = Cup.objects.filter(competition=login_team.competition)
        print(teams)
        is_play = len(Cup.objects.filter(team=login_team)) > 0
        context = {
            'login_team': login_team,
            'teams': teams,
            'is_play': is_play,
        }
        if login_team.competition.competition_level < 3:
            template = loader.get_template('SPC_main/cup.html')
        else:
            template = loader.get_template('SPC_main/cup_iac.html')
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        print("POST", request.POST)


@csrf_exempt
def add_team_to_cup(request):
    login_team = request.user.Teams.all()[0]
    if len(Cup.objects.filter(team=login_team)) == 0:
        t = Cup(team=login_team, competition=login_team.competition, cup_number=1)
        t.save()
        return JsonResponse({
            'status': "Success"
        })
    return JsonResponse({
        'status': 'failed'
    })

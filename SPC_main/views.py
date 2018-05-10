from django.shortcuts import render, HttpResponseRedirect, loader, HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from register.models import Team


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


def table_view(request):
    login_team = request.user.Teams.all()[0]
    teams = Team.objects.filter(competition=login_team.competition)
    print(len(list(teams)))
    context = {
        'login_team': login_team,
        'teams': teams
    }
    template = loader.get_template('SPC_main/table-spc.html')
    return HttpResponse(template.render(context, request))

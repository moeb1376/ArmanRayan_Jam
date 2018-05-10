import random
import subprocess
from itertools import chain
from django.utils.timezone import now

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, loader, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from register.models import auth_user, Team
from .models import Match
from .forms import *


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def online_match(request):
    team = request.user.Teams.all()[0]
    code = team.Team_Code.all()
    print(code)
    context = {
        'team': team,
        'codes': list(code)
    }
    template = loader.get_template('online_match/play.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login', redirect_field_name='')
def play_online_ajax(request):
    user_team = request.user.Teams.all()[0]
    if len(Match.objects.filter(team2=user_team.id, is_running=True)) > 0:
        print("Start new game filed: Game is running")
        return JsonResponse({"status": "Failed",
                             "error": "Game is running"})
    play_mode = request.GET.get('play')
    print(type(play_mode))
    loading = "<img src='statics/img/loading_gif/2.gif'>"
    if play_mode == '1':
        print('Armankadeh')
        data = {
            'random_loading': loading
        }
        t = Team.objects.get(pk=20)
        print(t)
        m = Match(team1=Team.objects.get(pk=20), team2=user_team, is_running=True)
        m.save()
        s = subprocess.Popen(
            ['bash', '/home/moeb/PycharmProjects/ArmanRayan_Jam/test_bash/Online.sh', str(20), str(user_team.id)])
    else:
        print("Random")
        same_competition_teams = Team.objects.filter(
            competition__competition_level=user_team.competition.competition_level)
        print(len(same_competition_teams))
        random_team_id = random.randint(0, len(same_competition_teams) - 1)
        random_team = same_competition_teams[random_team_id]
        while random_team.id == user_team.id or len(Code.objects.filter(team=random_team)) == 0:
            random_team_id = random.randint(0, len(same_competition_teams) - 1)
            random_team = same_competition_teams[random_team_id]
        random_team_last_version = random_team.code_address
        user_team_last_version = user_team.code_address
        print(random_team_id, random_team, user_team.id, user_team_last_version, random_team_last_version)
        data = {
            "team_name": random_team.user_team.username,
            "university": random_team.university.university_name,
            'image_url': random_team.logo_image.url,
            'random_loading': loading % random.randint(1, 3)
        }
        # m = Match(team1=random_team, team2=user_team, is_running=True)
        # m.save()
    return JsonResponse(data)


def test(request):
    template = loader.get_template('online_match/login_se.html')
    return HttpResponse(template.render({}, request))


def upload_view(request):
    print(request)
    if request.method == 'POST':
        form = CodeUploadForm(data=request.POST, files=request.FILES)
        team = request.user.Teams.all()[0]
        codes = Code.objects.filter(team=team.id)
        if len(codes) >= 5:
            firs_code = min(codes, key=lambda x: x.id)
            firs_code.delete()
        last_version = max(codes, key=lambda x: x.version, default=0)
        if not isinstance(last_version, int):
            last_version = last_version.version
        if form.is_valid():
            f = form.save(commit=False)
            f.version = last_version + 1
            f.team = team
            f.save()
            return JsonResponse({"success": True})
        else:
            print('invalid form')
            print(form.errors)
            return JsonResponse({"success": False})
    elif request.method == "GET":
        template = loader.get_template('online_match/upload_ajax.html')
        return HttpResponse(template.render({}, request))
        # return HttpResponseRedirect("/jaam")


def log_view(request):
    template = loader.get_template('online_match/log.html')
    team = request.user.Teams.all()[0]
    logs1 = Match.objects.filter(team1=team).only("team2", "is_running", "log_file", "winner", "date")
    logs2 = Match.objects.filter(team2=team).only("team1", "is_running", "log_file", "winner", "date")
    context = {
        'team': team,
        "log_away": logs1,
        "log_home":logs2,
    }
    return HttpResponse(template.render(context, request))

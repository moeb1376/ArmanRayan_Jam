import random
import subprocess
import json
from itertools import chain

import re

import os
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, loader, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
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
    if team.competition.competition_level < 3:
        template = loader.get_template('online_match/play.html')
    else:
        template = loader.get_template('online_match/play_iac.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login', redirect_field_name='')
def play_online_ajax(request):
    user_team = request.user.Teams.all()[0]
    if len(Match.objects.filter(team2=user_team.id, is_running=True)) > 0:
        print("Start new game filed: Game is running")
        return JsonResponse({"status": "Failed",
                             "error": "Game is running"})
    play_mode = request.GET.get('play')
    selected_code = request.GET.get('team_selected_code')
    team_name, version = re.search(r'(.*)\ \|\ [vV]([0-9]*)', selected_code).groups()
    team2_code = Code.objects.filter(team=user_team, version=version)[0]
    loading = "<img src='statics/img/loading_gif/2.gif'>"
    if play_mode == '1':
        print('Armankadeh')
        data = {
            'random_loading': loading
        }
        armankadeh_team_str = "armankadeh_1" if user_team.competition.competition_level == 1 else "armankadeh_2"
        armankadeh_team = Team.objects.get(user_team__username=armankadeh_team_str)
        m = Match(team1=armankadeh_team, team2=user_team, is_running=True)
        m.save()
        bash_file_base_dir = settings.BASE_DIR + '/online_match/ports/5000'
        s = subprocess.Popen(
            ['bash', bash_file_base_dir + '/Mys.sh', bash_file_base_dir, armankadeh_team.language.language_name,
             user_team.language.language_name])
        m.is_running = False
        m.save()
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
            'random_loading': loading
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
    if team.competition.competition_level >= 3:
        raise Http404('این صفحه مخصوص مسابقات spc است.')
    logs1 = Match.objects.filter(team1=team).only("team2", "is_running", "log_file", "winner", "date")
    logs2 = Match.objects.filter(team2=team).only("team1", "is_running", "log_file", "winner", "date")
    context = {
        'team': team,
        "log_away": logs1,
        "log_home": logs2,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def online_match_result(request):
    print(request)
    s = request.body
    print(request.body)
    data = json.loads(s.decode('utf8').replace("\'", "\""))
    print(data)
    # m = Match.objects.filter(team1__pk=data['team1'], team2__pk=data['team2'], is_running=True).last()
    # if m is not None:
    #     m.is_running = False
    #     m.save()
    return JsonResponse({"a": "k"})

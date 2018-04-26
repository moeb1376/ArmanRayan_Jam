import random
import subprocess

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, loader, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from register.models import auth_user, Team
from .models import Match
from .forms import *


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def online_match(request):
    team = request.user.Teams.all()[0]
    code = team.Team_Code.all()
    print(code)
    if len(code) == 0:
        context = {
            'team': team,
            'codes': list(code)
        }
        template = loader.get_template('online_match/play.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("jaam")


@login_required(login_url='/login', redirect_field_name='')
def play_online_ajax(request):
    id_team = request.user.id
    play_mode = request.GET.get('play')
    print(type(play_mode))
    loading = "<img src='statics/img/loading_gif/%d.gif'>"
    if play_mode == '1':
        print('Armankadeh')
        data = {
            'random_loading': loading % random.randint(1, 3)
        }
        t = Team.objects.get(pk=20)
        print(t)
        team2 = request.user.Teams.all()[0]
        m = Match(team1=Team.objects.get(pk=20), team2=team2, is_running=True)
        m.save()
        s = subprocess.Popen(
            ['bash', '/home/moeb/PycharmProjects/ArmanRayan_Jam/test_bash/Online.sh', str(20), str(team2.id)])
    else:
        print("Random")
        random_team_id = random.randint(0, Team.objects.count() - 1)
        random_team = Team.objects.all()[random_team_id]
        while random_team.id == id_team:
            random_team_id = random.randint(0, Team.objects.count() - 1)
            random_team = Team.objects.all()[random_team_id]
        print(random_team_id, random_team, id_team)
        data = {
            "team_name": random_team.user_team.username,
            "university": random_team.university.university_name,
            'image_url': random_team.logo_image.url,
            'random_loading': loading % random.randint(1, 3)
        }
        m = Match(team1=random_team, team2=request.user.Teams.all()[0], is_running=True)
        m.save()
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

import random
import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import Http404, HttpResponse, loader

from register.models import Team
from .models import Match
# from .tasks import start_game
from .forms import *

counter = 0


@login_required(login_url='/login', redirect_field_name='')
def online_match(request):
    team = request.user.Teams.all()[0]
    team_competition = team.competition.competition_level
    context = {'login_team': team}
    if team_competition < 3:
        code = team.Team_Code.filter(human_checked=True)
        print(code)
        context['codes'] = code
        if request.get_full_path() == '/old_play/':
            template = loader.get_template('Old/extend/play_spc.html')
        else:
            template = loader.get_template('2.1/online_match.html')
    else:
        if team_competition == 3:
            context['data_set1'] = '/media/DataSet/Text/v1-3000.rar'
            context['data_set2'] = '/media/DataSet/Text/v3001-6000.rar'
            context['data_set3'] = '/media/DataSet/Text/v6001-9000.rar'
        elif team_competition == 4:
            context['data_set1'] = '/media/DataSet/Sound/0.rar'
            context['data_set2'] = '/media/DataSet/Sound/1.rar'
            context['data_set3'] = '/media/DataSet/Sound/2.rar'
            context['help'] = '/media/DataSet/Sound/htkbook.pdf'
        else:
            context['data_set1'] = '/media/DataSet/Picture/t1.rar'
            context['data_set2'] = '/media/DataSet/Picture/t2.rar'
            context['data_set3'] = '/media/DataSet/Picture/t3.rar'
            context['public_test'] = '/media/DataSet/Picture/challenge.tar.gz'
        if request.get_full_path() == '/old_play':
            template = loader.get_template('Old/extend/play_iac.html')
        else:
            template = loader.get_template('2.0/friendly_IAC.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login', redirect_field_name='')
def play_online_ajax(request):
    user_team = request.user.Teams.all()[0]
    if len(Match.objects.filter(team2=user_team.id, is_running=True)) > 0:
        print("Start new game failed: Game is running")
        return JsonResponse({"status": "Failed",
                             "error": "Game is running"})
    play_mode = request.GET.get('play')
    selected_code = request.GET.get('team_selected_code')
    team_name, version = re.search(
        r'(.*)\ \|\ [vV]([0-9]*)', selected_code).groups()
    user_team_code = Code.objects.filter(team=user_team, version=version)[0]
    loading = "<img src='statics/img/loading_gif/2.gif'>"
    if play_mode == '1':
        print('Armankadeh')
        data = {
            'random_loading': loading
        }
        armankadeh_team_str = "armankadeh_1" if user_team.competition.competition_level == 1 else "armankadeh_2"
        armankadeh_team = Team.objects.get(user_team__username=armankadeh_team_str)
        # result = start_game.delay(user_team.id, armankadeh_team.id, user_team_code.code.path,
        #                           armankadeh_team.code_address)
    else:
        print("Random")
        same_competition_teams = Team.objects.filter(
            competition__competition_level=user_team.competition.competition_level,
            code_address__isnull=False)
        print(len(same_competition_teams))
        if same_competition_teams == 0:
            print("Start new game failed: Game is running")
            return JsonResponse({"status": "Failed",
                                 "error": "Opponent not find"})
        random_team_list = random.sample(range(len(same_competition_teams)), len(same_competition_teams) - 1)
        random_team_index = random_team_list.pop()
        random_team = same_competition_teams[random_team_index]
        while random_team.id == user_team.id or len(Code.objects.filter(team=random_team, human_checked=True)) == 0:
            if len(random_team_list) == 0:
                print("Start new game failed: Game is running")
                return JsonResponse({"status": "Failed",
                                     "error": "Opponent not find"})
            random_team_index = random_team_list.pop()
            random_team = same_competition_teams[random_team_index]
        data = {
            "team_name": random_team.user_team.username,
            "university": random_team.university.university_name,
            'image_url': random_team.logo_image.url,
            'random_loading': loading
        }
        random_team_code = Code.objects.filter(team=random_team, human_checked=True).order_by(id)
        # start_game.delay(user_team, random_team, user_team_code, random_team_code)
    return JsonResponse(data)


def upload_view(request):
    print(request)
    if request.method == 'POST':
        form = CodeUploadForm(data=request.POST, files=request.FILES)
        team = request.user.Teams.all()[0]
        codes = Code.objects.filter(team=team.id)
        if len(codes) >= 5:
            first_code = min(codes, key=lambda x: x.id)
            first_code.delete()
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
        template = loader.get_template('2.0/upload_ajax.html')
        return HttpResponse(template.render({}, request))


def log_view(request):
    if request.get_full_path() == '/old_log':
        template = loader.get_template('Old/extend/log.html')
    else:
        template = loader.get_template('2.1/log.html')
    team = request.user.Teams.all()[0]
    if team.competition.competition_level >= 3:
        raise Http404('این صفحه مخصوص مسابقات spc است.')
    logs1 = Match.objects.filter(team1=team).only(
        "team2", "is_running", "log_file", "winner", "date")
    logs2 = Match.objects.filter(team2=team).only(
        "team1", "is_running", "log_file", "winner", "date")
    context = {
        'login_team': team,
        "log_away": logs1,
        "log_home": logs2,
    }
    return HttpResponse(template.render(context, request))

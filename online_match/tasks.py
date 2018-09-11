import os
import re
import shutil
import subprocess
import signal
import time
from threading import Condition, Thread

from django.conf import settings

import online_match.ports.server.server as server
from celery import task
from online_match.ports.server.CONST import ServerSocket
from register.models import Team
from .models import Match


def loading_teams_code(src_team1, src_team2):
    print("in loading teams code ")
    src1 = re.search(r'(.+)\.(.+)', src_team1).groups()[0]
    src2 = re.search(r'(.+)\.(.+)', src_team2).groups()[0]
    server_base_dir = os.path.join(os.path.join(
        settings.BASE_DIR, 'online_match'), 'ports')
    client_base_dir_template = os.path.join(server_base_dir, 'client') + '%d'
    if os.path.isdir(client_base_dir_template % 1):
        shutil.rmtree(client_base_dir_template % 1)
    if os.path.isdir(client_base_dir_template % 2):
        shutil.rmtree(client_base_dir_template % 2)
    client_dst = [client_base_dir_template % 1, client_base_dir_template % 2]
    shutil.copytree(os.path.join(settings.MEDIA_ROOT, src1), client_dst[0])
    shutil.copytree(os.path.join(settings.MEDIA_ROOT, src2), client_dst[1])
    return client_dst


def loading_log_file(src, dst):
    temp = os.path.split(dst)
    if not os.path.isdir(temp[0]):
        os.mkdir(temp[0])
    try:
        shutil.move(src, dst)
    except Exception as e:
        return False
    else:
        return True


def kill_celery_child():
    celery_PID = int(open('celery_pid','r').readline())
    os.system('pkill -9 -P %d' % celery_PID)


@task(bind=True, time_limit=2000)
def start_game(self, team1_id, team2_id, team1_code_src, team2_code_src):
    team1 = Team.objects.get(pk=team1_id)
    team2 = Team.objects.get(pk=team2_id)
    languages = [team1.language.language_name, team2.language.language_name]
    team1_code_src = os.path.join(settings.MEDIA_ROOT, team1_code_src)
    m = Match(team1=team1, team2=team2, is_running=True)
    m.save()
    cv = Condition()
    winner = [0, ]
    print("loading team code ....", end=' ')
    client_dst = loading_teams_code(team1_code_src, team2_code_src)
    print("Complete")
    game_manager = server.GameManager(cv)
    bash_file_base_dir = settings.BASE_DIR + '/online_match/ports'
    t = Thread(target=game_manager.start, args=(winner,))
    print("start server ....", end=' ')
    t.start()
    print("Complete")
    print("start clients ....", end=' ')
    clients_process = [0, 0]
    for i in range(2):
        clients_process[i] = subprocess.Popen(['bash', bash_file_base_dir + '/Client.sh',
                                               client_dst[i], languages[i], str(i)])
        with cv:
            flag = cv.wait(timeout=ServerSocket.TIME_OUT // 2)
        if flag:
            print("Player %d connect" % i, end=' , ')
        else:
            print("player %d lose" % i)
            winner[0] = 2 - i
            m.description = "team %d connection lost" % (i + 1)
            break
    print("Complete")
    d = t.join()
    for i in clients_process:
        os.kill(i.pid, signal.SIGTERM)
    m.winner = winner[0]
    src_log = settings.BASE_DIR + '/online_match/ports/server/test.AbaloneLog'
    date = time.strftime("%y%m%d_%H%M%S")
    match_teams = "%s_VS_%s" % (team1.user_team.username, team2.user_team.username)
    log_file_name = "%s_%s" % (match_teams, date)
    game_name = "Agon" if team1.competition.competition_level == 1 else "Abalone"
    file_url = '/LogFile/%s/%s/%s.%sLog' % (game_name, match_teams, log_file_name, game_name)
    dst_log = (settings.MEDIA_ROOT + file_url)
    if loading_log_file(src_log, dst_log):
        print("loading log file is complete")
    else:
        print("loading file is failed")
    m.log_file = '/media' + file_url
    m.is_running = False
    m.save()
    print("match end ", m)
    kill_celery_child()
    return True

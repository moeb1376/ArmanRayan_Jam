from django.shortcuts import render, HttpResponseRedirect, loader, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here

@login_required(login_url='/login', redirect_field_name='')
def SPC_main_page(request):
    print(request.user)
    team = request.user.Teams.all()[0]
    team_member = team.Users.all()
    if len(team_member) < 2:
        return HttpResponseRedirect('/setting')
    for member in team_member:
        print(member.user_lname)
    context = {
        'team': team,
        'members': team_member
    }
    template = loader.get_template('SPC_main/jaam2.html')
    return HttpResponse(template.render(context, request))


def team_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

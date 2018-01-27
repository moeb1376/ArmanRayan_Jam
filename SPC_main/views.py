from django.shortcuts import render, HttpResponseRedirect, loader, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here

@login_required(login_url='/login', redirect_field_name='')
def SPC_main_page(request):
    print(request.user)
    team = request.user.team_set.all()[0]
    team_member = team.user_set.all()
    for member in team_member:
        print(member.user_lname)
    context = {
        'team': team,
        'members': team_member
    }
    template = loader.get_template('SPC_main/jaam.html')
    return HttpResponse(template.render(context, request))


def team_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

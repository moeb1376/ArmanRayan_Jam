from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import *
from django.forms import modelformset_factory


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def setting_page(request):
    redirect_flag = False
    team_change = request.user.Teams.all()[0]
    user_formset_factory = modelformset_factory(User, exclude=['is_head', 'team'],
                                                extra=3 - len(team_change.Users.all()),
                                                labels=UserSettingForm.label,
                                                )
    if request.method == 'POST':
        print(request.POST)
        auth_user_setting_form = UserTeamSettingForm(request.POST, instance=request.user)
        if auth_user_setting_form.is_valid():
            print('auth user is valid ')
        else:
            print('auth user is not valid', auth_user_setting_form.cleaned_data, auth_user_setting_form.errors)
        team_setting_form = TeamSettingForm(request.POST)
        if team_setting_form.is_valid():
            test = team_setting_form.save(commit=False)
        else:
            print(team_setting_form.errors)
            test = [team_setting_form, 'WTFaaz']

        user_team_form = []
        for i in range(3):
            user_team_form.append(UserSettingForm(request.POST))
        print("****")
        print(test)
    else:
        redirect_flag = True
        auth_user_setting_form = UserTeamSettingForm(request.POST or None, instance=request.user)
        team_setting_form = TeamSettingForm(instance=team_change)
        team_setting_form.change_required_field()
        user_team_form = user_formset_factory(queryset=team_change.Users.all())
        # user_team_form = []
        # for i in team_change.Users.all():
        #     user_team_form.append(UserSettingForm(instance=i))
        # for i in range(3 - len(team_change.Users.all())):
        #     user_team_form.append(UserSettingForm())
        # user_team_form[1].change_required_user()
        # user_team_form[2].change_required_user()
    template = loader.get_template('settings.html')
    # print(request.user.Teams.all()[0].university)
    # print(request.user.Teams.all()[0].Users.all()[0])
    return HttpResponse(
        template.render({'test': redirect_flag, 'user_form': user_team_form, 'auth_form': auth_user_setting_form,
                         'team_form': team_setting_form, 'testForm': testForm()}, request))

# def test_change(request):
#     if request.method == 'POST':
#         form = test_change_form(request.POST, instance=request.user)
#         if form.is_valid():
#             print('hoooooraaaaaaay')
#         else:
#             print(':|:|:|:|:|:|:|:|:|:|:|:|')
#     else:
#         form = test_change_form(instance=request.user)
#     template = loader.get_template('test.html')
#     return HttpResponse(template.render({'form': form}, request))

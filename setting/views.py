import os
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .forms import *
from django.forms import modelformset_factory
from django.conf import settings
from PIL import Image


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def setting_page(request, active_member=0):
    team_change = request.user.Teams.all()[0]
    if team_change.competition.competition_level < 3:
        user_formset_factory = modelformset_factory(MyUser, extra=3, max_num=3, form=UserSettingForm)
    else:
        user_formset_factory = modelformset_factory(MyUser, extra=2, max_num=2, form=UserSettingForm)
    if request.method == 'POST':
        print(request.POST)
        auth_user_setting_form = UserTeamSettingForm(request.POST, instance=request.user)
        if auth_user_setting_form.is_valid():
            print('auth user is valid ')
            auth_user_setting_form.save()
        else:
            print('auth user is not valid', auth_user_setting_form.cleaned_data, auth_user_setting_form.errors)
        previous_logo_image = '/'.join(team_change.logo_image.url.split('/')[2:])
        team_setting_form = TeamSettingForm(request.POST or None, request.FILES or None, instance=team_change)
        team_setting_form.change_required_field()
        team_setting_form.change_empty_label()
        print(settings.LOGO_DEFAULT, os.path.join(settings.MEDIA_ROOT, previous_logo_image), previous_logo_image)
        if team_setting_form.is_valid():
            print('team setting form is valid ')
            if 'logo_image' in team_setting_form.changed_data:
                previous_logo_image_path = os.path.join(settings.MEDIA_ROOT, previous_logo_image)
                if os.path.isfile(previous_logo_image_path) and previous_logo_image_path != settings.LOGO_DEFAULT:
                    os.remove(previous_logo_image_path)
            print(team_setting_form)
            s = team_setting_form.save()
            if 'logo_image' in team_setting_form.changed_data:
                print(s.logo_image.path)
                crop_image(s.logo_image.path)
            else:
                print(s.logo_image.path)
        else:
            print(team_setting_form.errors)
        user_team_form = user_formset_factory(request.POST, queryset=team_change.Users.all())
        for index, user_team in enumerate(user_team_form):
            print('user_team', user_team.has_changed(), user_team.changed_data)
            if not user_team.is_valid():
                print('user fname:', user_team.cleaned_data)
            else:
                if user_team.cleaned_data.get('user_fname', '') == '' and \
                        user_team.cleaned_data.get('user_lname', '') == '':
                    continue
                temp = user_team.save(commit=False)
                temp.is_head = True if index == 0 else False
                temp.team = team_change
                temp.save()
                print('temp:', temp, temp.id)
        user_team_form = user_formset_factory(queryset=team_change.Users.all())
    else:
        auth_user_setting_form = UserTeamSettingForm(request.POST or None, instance=request.user)
        team_setting_form = TeamSettingForm(instance=team_change)
        team_setting_form.change_required_field()
        team_setting_form.change_empty_label()
        user_team_form = user_formset_factory(queryset=team_change.Users.all())
        for i in user_team_form:
            i.change_empty_label()
        for field in auth_user_setting_form.fields:
            auth_user_setting_form.fields[field].widget.attrs['class'] = "validate"
        for field in team_setting_form.fields:
            team_setting_form.fields[field].widget.attrs['class'] = "validate"
        for user_form in user_team_form:
            for field in user_form.fields:
                user_form.fields[field].widget.attrs["class"] = "validate"
    team = request.user.Teams.all()[0]
    print(request.get_full_path())
    if team.competition.competition_level < 3:
        if request.get_full_path() == '/old_setting/':
            template = loader.get_template('Old/settings.html')
        else:
            template = loader.get_template("2.1/setting.html")
    else:
        if request.get_full_path() == '/old_setting/':
            template = loader.get_template('Old/settings_iac.html')
        else:
            template = loader.get_template("2.1/setting.html")

    user_require = 2 if team.competition.competition_level < 3 else 1
    redirect_flag = False if len(team_change.Users.all()) >= user_require else True
    print('redirect ', redirect_flag, user_require)
    active_member = int(active_member) if (active_member and int(active_member)< 4) else 0
    context = {
        'test': redirect_flag,
        'user_form': user_team_form,
        'auth_form': auth_user_setting_form,
        'team_form': team_setting_form,
        "login_team": team_change,
        "active_member": active_member,
    }
    return HttpResponse(
        template.render(context, request))


def crop_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    if min(width, height) == height:
        temp = image.crop(((width - height) / 2, 0, (width + height) / 2, height))
    else:
        temp = image.crop((0, (height - width) / 2, width, (height + width) / 2))
    print(temp)
    temp.resize((300, 300)).save(image_path)


def test_ajax(request):
    username = request.GET.get('username')
    print(request.GET, request.user)
    data = {
        'is_taken': auth_user.objects.filter(username=username).exists(),
        'logo_image': auth_user.objects.filter(username=username)[0].Teams.all()
    }
    return JsonResponse(data)


def mentor_ajax(request):
    mentor_code = request.GET.get('mentor_code')
    print(mentor_code)
    response = {
        'find_mentor': False,
    }
    if len(mentor_code) < 6:
        return JsonResponse(response)
    if len(Mentor.objects.filter(code=mentor_code)) == 0:
        return JsonResponse(response)
    response['find_mentor'] = True
    return JsonResponse(response)

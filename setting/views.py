import os
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .forms import *
from django.forms import modelformset_factory
from django.conf import settings


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def setting_page(request):
    redirect_flag = False
    team_change = request.user.Teams.all()[0]
    user_formset_factory = modelformset_factory(MyUser, extra=3, max_num=3, form=UserSettingForm)
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
        if team_setting_form.is_valid():
            print('team setting form is valid ')
            if 'logo_image' in team_setting_form.changed_data:
                if os.path.isfile(os.path.join(settings.MEDIA_ROOT,previous_logo_image)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, previous_logo_image))
            team_setting_form.save()
        else:
            print(team_setting_form.errors)
        user_team_form = user_formset_factory(request.POST, queryset=team_change.Users.all())
        for user_team in user_team_form:
            type(user_team)
            if not user_team.is_valid():
                print('user fname:', user_team.cleaned_data)
            else:
                if user_team.cleaned_data.get('user_fname', '') == '' and \
                                user_team.cleaned_data.get('user_lname', '') == '':
                    continue
                temp = user_team.save(commit=False)
                temp.team = team_change
                temp.save()
                print('temp:', type(temp))
        if user_team_form.is_valid():
            print("Pashm")
        else:
            print(user_team_form.errors)
    else:
        redirect_flag = True
        auth_user_setting_form = UserTeamSettingForm(request.POST or None, instance=request.user)
        team_setting_form = TeamSettingForm(instance=team_change)
        team_setting_form.change_required_field()
        user_team_form = user_formset_factory(queryset=team_change.Users.all())
    template = loader.get_template('settings.html')
    return HttpResponse(
        template.render({'test': redirect_flag, 'user_form': user_team_form, 'auth_form': auth_user_setting_form,
                         'team_form': team_setting_form}, request))


def test_change(request):
    if request.method == 'POST':
        form = test_change_form(request.POST, instance=request.user)
        if form.is_valid():
            print('hoooooraaaaaaay')
            form.save()
        else:
            print(':|:|:|:|:|:|:|:|:|:|:|:|')
    else:
        form = test_change_form(instance=request.user)
    template = loader.get_template('test.html')
    return HttpResponse(template.render({'form': form}, request))


def test_image_field(request):
    print(settings.BASE_DIR)
    print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    print(settings.STATIC_ROOT)
    instance = Test.objects.get(id=8)
    print('instance ', instance.image.url)
    if request.method == 'POST':
        form = testForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            print('hooray')
            print(form)
            form.save()
        else:
            print(form.errors)
            print(':(')
    else:
        form = testForm(instance=instance)
    template = loader.get_template('test.html')
    print('tahesh ', form.fields['image'])
    return HttpResponse(template.render({'form': form}, request))

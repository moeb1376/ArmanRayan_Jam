from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import *
from django.forms import modelformset_factory, inlineformset_factory
from django.conf import settings


# Create your views here.
@login_required(login_url='/login', redirect_field_name='')
def setting_page(request):
    redirect_flag = False
    team_change = request.user.Teams.all()[0]
    user_formset_factory = modelformset_factory(MyUser,
                                                # fields=['user_fname', 'user_lname', 'email', 'university', 'grade',
                                                #         'entrance_year', 'graduate_year', 'skills'],
                                                extra=3,
                                                max_num=3,
                                                # labels=UserSettingForm.label,
                                                form=UserSettingForm
                                                )

    # user_formset_inline = inlineformset_factory(Grade, MyUser, form=UserSettingForm, extra=3, max_num=3)

    if request.method == 'POST':
        print(request.POST)
        auth_user_setting_form = UserTeamSettingForm(request.POST, instance=request.user)
        if auth_user_setting_form.is_valid():
            print('auth user is valid ')
            # auth_user_setting_form.save()
        else:
            print('auth user is not valid', auth_user_setting_form.cleaned_data, auth_user_setting_form.errors)
        team_setting_form = TeamSettingForm(request.POST, instance=team_change)
        team_setting_form.change_required_field()
        if team_setting_form.is_valid():
            print('team setting form is valid ')
            # test = team_setting_form.save(commit=False)
        else:
            print(team_setting_form.errors)
            test = [team_setting_form, 'WTFaaz']

        user_team_form = user_formset_factory(request.POST, queryset=team_change.Users.all())
        c = 0
        queryset = team_change.Users.all()
        for userman in user_team_form:
            print(userman.fields['id'], queryset[c].id)
            if not userman.fields['id'].initial:
                print('dasti')
                userman.fields['id'].initial = queryset[c].id
            else:
                print('payi')
            c += 1
        print('salam:', team_change.Users.all()[0].id, user_team_form[0].fields['id'])
        for userman in user_team_form:
            type(userman)
            if not userman.is_valid():
                print('user fname:', userman.cleaned_data)
            else:
                temp = userman.save(commit=False)
                temp.team = team_change
                temp.save()
                print('temp:', type(temp))
            c += 1
        if user_team_form.is_valid():
            print("Pashm")
        else:
            print(user_team_form.errors)
        print("****")
        # print(test)
    else:
        redirect_flag = True
        auth_user_setting_form = UserTeamSettingForm(request.POST or None, instance=request.user)
        team_setting_form = TeamSettingForm(instance=team_change)
        team_setting_form.change_required_field()
        user_team_form = user_formset_factory(queryset=team_change.Users.all())
        # user_team_inlineform = user_formset_inline(queryset=team_change.Users.all())
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

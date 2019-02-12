from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import BaseModelFormSet

from .models import *


class UserSettingForm(forms.ModelForm):
    label = {
        'user_fname': 'نام',
        'user_lname': "نام خانوادگی",
        'email': "رایانامه",
        'university': 'دانشگاه',
        'grade': 'مقطع',
        'entrance_year': 'ورودی',
        'graduate_year': "فارغ‌التحصیل",
        'skills': "توانایی‌ها"
    }

    def change_required_user(self):
        self.fields['user_fname'].required = False
        self.fields['user_lname'].required = False
        self.fields['email'].required = False
        self.fields['university'].required = False
        self.fields['grade'].required = False
        self.fields['entrance_year'].required = False
        self.fields['graduate_year'].required = False
        self.fields['skills'].required = False

    def change_empty_label(self):
        self.fields['university'].empty_label = "دانشگاه"
        self.fields['grade'].empty_label = "مقطع"

    class Meta:
        model = MyUser
        exclude = ['is_head', 'team']
        labels = {
            'user_fname': 'نام',
            'user_lname': "نام خانوادگی",
            'email': "رایانامه",
            'university': 'دانشگاه',
            'grade': 'مقطع',
            'entrance_year': 'ورودی',
            'graduate_year': "فارغ‌التحصیل",
            'skills': "توانایی‌ها"
        }


class UserTeamSettingForm(UserChangeForm):
    # def is_valid(self):
    #     valid = super().is_valid()
    #     print('self . eroors ', dict(self.errors))
    #     if dict(self.errors).get('username', '') != '' and len(
    #             list(dict(self.errors).keys()).pop(list(dict(self.errors)).index('username'))) == 0:
    #         return True
    #     return valid

    class Meta:
        model = auth_user
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'نام',
            'email': 'رایانامه'
        }


class TeamSettingForm(forms.ModelForm):
    def change_required_field(self):
        self.fields['team_bio'].required = False
        self.fields['logo_image'].required = False
        self.fields['mentor'].required = False

    def change_empty_label(self):
        self.fields['university'].empty_label = "دانشگاه"

    class Meta:
        model = Team
        fields = ['university', 'team_bio', 'logo_image', 'mentor','phone_number']
        labels = {
            'university': 'دانشگاه',
            'team_bio': "بیو",
            'logo_image': "انتخاب عکس",
            'mentor': "کد معرفی",
            'phone_number':"شماره تماس"
        }
        widgets = {
            'logo_image': forms.FileInput
        }


class test_change_form(UserChangeForm):
    class Meta:
        model = auth_user
        fields = (
            'username',
            'email',
            'password'
        )

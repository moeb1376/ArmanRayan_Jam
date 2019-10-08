from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import BaseModelFormSet

from .models import *


class UserSettingForm(forms.ModelForm):

    def change_empty_label(self):
        self.fields['university'].empty_label = "دانشگاه"
        self.fields['grade'].empty_label = "مقطع"

    class Meta:
        model = MyUser
        exclude = ['is_head', 'team', 'graduate_year']


class UserTeamSettingForm(UserChangeForm):
    class Meta:
        model = auth_user
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'نام',
            'email': 'رایانامه'
        }


class TeamSettingForm(forms.ModelForm):

    def change_empty_label(self):
        self.fields['university'].empty_label = "دانشگاه"

    class Meta:
        model = Team
        fields = ['university', 'team_bio', 'logo_image', 'mentor', 'phone_number']
        labels = {
            'university': 'دانشگاه',
            'team_bio': "بیو",
            'logo_image': "انتخاب عکس",
            'mentor': "کد معرفی",
            'phone_number': "شماره تماس"
        }
        widgets = {
            'logo_image': forms.FileInput
        }

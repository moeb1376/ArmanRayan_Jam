from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    def changed_password_label(self):
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'

    class Meta:
        model = auth_user
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': "نام تیم",
            'email': "رایانامه",
        }


class TeamForm(forms.ModelForm):
    checkbox = forms.BooleanField(label='شرایط را قبول دارم')

    def changed_required_mentor(self):
        self.fields['mentor'].required = False
        self.fields['phone_number'].required = False

    def change_empty_label(self):
        self.fields['university'].empty_label = "دانشگاه"
        self.fields['competition'].empty_label = "مسابقه"
        self.fields['language'].empty_label = "زبان برنامه‌نویسی"

    class Meta:
        model = Team
        fields = {'university', 'competition', 'language', 'mentor', 'phone_number'}
        labels = {
            'mentor': 'کد معرفی(اختیاری)',
            'phone_number': 'شماره تماس (اختیاری)'
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام تیم یا رایانامه تیم', required=True)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput, required=True)

    class Meta:
        help_texts = {
            'username': 'Some useful help username text.',
            'password': 'Some password help text.'
        }

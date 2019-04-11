from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from Jam.settings import EMAIL_HOST_USER
from .models import Cup, Key, Team
import hashlib


def get_key(request):
    print(request.GET)
    user = request.GET.get("user")
    cup = request.GET.get("cup")
    user_object = Team.objects.get(id=user)
    cup_object = Cup.objects.get(id=cup)
    user_keys = Key.objects.filter(team=user_object)
    if cup_object.end_date < timezone.now():
        return JsonResponse({"id": 2, "msg": "cup expired"})
    if user_keys.filter(cup=cup_object).exists():
        return JsonResponse({"id": 3, "msg": "key for this cup generated"})
    string_key = user_object.user_team.username + cup_object.name
    key = hashlib.sha256(string_key.encode()).hexdigest()[0:25]
    temp = Key(team=user_object, cup=cup_object, key=key)
    temp.save()
    send_mail("کلید شرکت در Cup", "کلید شما برای شرکت در رقابت‌ %s :\n %s" % (cup_object.name, key), EMAIL_HOST_USER,
              [user_object.user_team.email, ])
    return JsonResponse({"id": 1, "msg": "Success", "key": key})


def connect(request):
    key = request.GET.get("key", None)
    if key is None:
        return JsonResponse({"id": 0, "msg": "bad request !!"})
    if not Key.objects.filter(key=key).exists():
        return JsonResponse({"id": 2, "msg": "Wrong Key !!"})
    key_object = Key.objects.get(key=key)
    if key_object.password_used:
        d = timezone.timedelta(minutes=30)
        print(timezone.now() - key_object.last_connection)
        print(timezone.now() - key_object.last_connection > d)
        print(d)
        return JsonResponse({"id": 3, "msg": "Password used"})
    key_object.password_used = True
    key_object.last_connection = timezone.now()
    key_object.save()
    return JsonResponse({"id": 1, "msg": "Connection Successfully!"})


def get_data(request):
    pass


def render_page(request):
    return render(request, "iac_cup.html")

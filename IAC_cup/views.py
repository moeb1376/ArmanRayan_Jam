from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from Jam.settings import EMAIL_HOST_USER
from .models import Cup, Key, Team, DatasetCup, UsersAnswer
import hashlib


def get_key(request):
    print(type(request.GET.get("cup")))
    # return JsonResponse({"test": "OK"})
    user = int(request.GET.get("user"))
    cup = int(request.GET.get("cup"))
    user_object = Team.objects.get(id=user)
    cup_object = Cup.objects.get(id=cup)
    user_keys = Key.objects.filter(team=user_object)
    if cup_object.end_date < timezone.now():
        return JsonResponse({"id": 2, "msg": "مدت زمان شرکت در این مسابقات پایان یافته است"})
    if user_keys.filter(cup=cup_object).exists():
        return JsonResponse({"id": 3,
                             "msg": "کلید برای این کاربر ارسال شده است. پوشه Spam خود را نیز چک کنید. در صورت عدم دریافت کلید با پشتیبانی سامانه در ارتباط باشید."})
    string_key = user_object.user_team.username + cup_object.name
    key = hashlib.sha256(string_key.encode()).hexdigest()[0:25]
    temp = Key(team=user_object, cup=cup_object, key=key)
    temp.save()
    send_mail("کلید شرکت در Cup", "کلید شما برای شرکت در رقابت‌ %s :\n %s" % (cup_object.name, key), EMAIL_HOST_USER,
              [user_object.user_team.email, ])
    return JsonResponse({"id": 1, "msg": "کلید با موفقیت ارسال شد"})


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
    message_id = request.GET.get("id", None)
    print(request.GET)
    if message_id is None:
        return JsonResponse({"id": 5, "msg": "bad request !!"})
    if message_id == '0':
        key = request.GET.get("key", None)
        player_id = request.GET.get("player_id", None)
        last_data_id = int(request.GET.get("last_data_id", None))
        if key is None or player_id is None or last_data_id is None:
            return JsonResponse({"id": 5, "msg": "bad request !!"})
        time_delta = timezone.timedelta(hours=1)
        try:
            key_object = Key.objects.get(key=key)
        except Exception as e:
            return JsonResponse({"id": 2, "msg": "This key is not exists"})
        if not key_object.password_used:
            return JsonResponse({"id": 3, "msg": "User not connect"})
        if timezone.now() - key_object.last_connection > time_delta:
            return JsonResponse({"id": 4, "msg": "Connection timeout"})
        if player_id != key_object.team.user_team.username:
            return JsonResponse({"id": 6, "msg": "Key or player name is not correct"})
        count = DatasetCup.objects.count()
        if last_data_id >= count:
            key_object.last_connection -= timezone.timedelta(hours=2)
            key_object.save()
            return JsonResponse({"id": 7, "msg": "The End!"})

        count = count if last_data_id + 10 > count else last_data_id + 10
        dataset = DatasetCup.objects.filter(cup=key_object.cup, id__range=[last_data_id + 1, count])
        result = []
        for data in dataset:
            if not UsersAnswer.objects.filter(data=data).exists():
                result.append({"id": data.id, "data": data.data})
                UsersAnswer(data=data, time_send=timezone.now(), user=key_object.team).save()
        if len(result):
            return JsonResponse({"id": 0, "msg": result})
        else:
            return JsonResponse({"id": 7, "msg": "It has been sent before"})
    else:
        key = request.GET.get("key", None)
        player_id = request.GET.get("player_id", None)
        answer_id = request.GET.get("answer_id", None)
        answer = request.GET.get("answer", None)
        if answer_id is None or key is None or player_id is None or answer is None:
            return JsonResponse({"id": 5, "msg": "bad request !!"})
        time_delta = timezone.timedelta(hours=1)
        try:
            key_object = Key.objects.get(key=key)
        except Exception as e:
            return JsonResponse({"id": 2, "msg": "This key is not exists"})
        if not key_object.password_used:
            return JsonResponse({"id": 3, "msg": "User not connect"})
        if timezone.now() - key_object.last_connection > time_delta:
            return JsonResponse({"id": 4, "msg": "Connection timeout"})
        if player_id != key_object.team.user_team.username:
            return JsonResponse({"id": 6, "msg": "Key or player name is not correct"})


def render_page(request):
    login_team = request.user.Teams.all()[0]
    competition_level = login_team.competition.competition_level
    cups = Cup.objects.filter(competition__competition_level=competition_level)
    return render(request, "iac_cup.html", {"cups": cups, "login_team": login_team})


def send_my_email(request):
    subject = "دادگان سری جدید"
    from_mail = EMAIL_HOST_USER
    to_mail = ["ebimosi14@gmail.com", "j.agheleh@yahoo.com"]
    body_text = "سری سوم و آخرین سری از دادگان مسابقه در سایت قرار داده شد.برای دانلود به سایت مسابقات مراجعه نمایید."
    body_text += "\n"
    body_text += "آخرین مهلت ارسال کدها تا ساعت ۲۳:۵۹ دقیقه روز ۴شنبه ۱۱ اردیبهشت می‌باشد."
    users = Team.objects.filter(competition__competition_level__gte=3)
    for my_user in users:
        message = EmailMultiAlternatives(subject=subject, body=body_text, from_email=from_mail,
                                         to=[my_user.user_team.email])
        html_message = get_template("email_template/message.html").render()
        message.attach_alternative(html_message, "text/html")
        message.send()
    message = EmailMultiAlternatives(subject=subject, body=body_text, from_email=from_mail, to=to_mail)
    html_message = get_template("email_template/message.html").render()
    message.attach_alternative(html_message, "text/html")
    message.send()
    return render(request, "email_template/message.html")

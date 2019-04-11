from django.shortcuts import render
from django.http import JsonResponse


def get_key(request):
    pass


def render_page(request):
    return render(request, "iac_cup.html")

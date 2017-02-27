import json
from django.shortcuts import render
from django.http import HttpResponse


from .utils import get_leaderboard, get_sorted_leaderboard


def home(request):
    return render(request, "index.html")


def leaderboard(request):
    data = get_leaderboard()
    data = json.dumps(data)

    return HttpResponse(data, content_type="application/json")


def sorted_leaderboard(request):
    sorted_data = get_sorted_leaderboard()
    data = json.dumps(sorted_data)
    return HttpResponse(data, content_type="application/json")
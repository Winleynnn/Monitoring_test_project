from django.shortcuts import render
from .models import Station_0020CF3B


def index(request):
    latest_twenty = Station_0020CF3B.objects.all()[1500:1550]
    return render(request, "polls/index.html", {'data' : latest_twenty})


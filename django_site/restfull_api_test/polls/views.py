from django.shortcuts import render
from .models import Data


def index(request):
    latest_twenty = Data.objects.all()[1500:1550]
    return render(request, "polls/index.html", {'data' : latest_twenty})


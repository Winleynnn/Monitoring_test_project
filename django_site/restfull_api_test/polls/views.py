from django.shortcuts import render
<<<<<<< HEAD
from .models import Station_0020CF3B


def index(request):
    latest_twenty = Station_0020CF3B.objects.all()[1500:1550]
    return render(request, "polls/index.html", {'data' : latest_twenty})
=======
from .models import Data
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    latest_twenty = Data.objects.all()[1500:1550]
    return render(request, "polls/header.html", {'data' : latest_twenty})
>>>>>>> authentication

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully")
    return redirect("/login")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                    template_name="polls/login.html",
                    context={"form": form})
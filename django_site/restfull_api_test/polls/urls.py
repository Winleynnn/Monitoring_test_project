from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('logout', views.logout_request, name = "Войти"),
    path('login', views.login_request, name = "Выйти"),
]
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('logout', views.logout_request, name = "Выйти"),
    path('login', views.login_request, name = "Войти"),
    path('register', views.register, name = "Регистрация"),
    path('feedbackform.html', views.feedback, name="Обратная связь"),
    path('station_admin', views.station_admin, name = "Админка"),
    path('station_admin/add', views.station_admin_add, name = 'upload'),
    path('404', views.not_found, name = "error")
]
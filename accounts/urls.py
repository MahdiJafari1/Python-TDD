from django.conf.urls import url
from django.urls import path
from accounts import views


urlpatterns = [
    path("send-email", views.send_login_email, name="send_login_email"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]
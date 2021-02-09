from django.urls import path, re_path
from . views import *

urlpatterns = [
    path("", index),
    path("register/", register),
    path("send-login-link/", send_login_link),
    path("login/token/<str:token>/", login_with_token),
    path("logout/", logout),
]
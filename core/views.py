from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import auth

from django.core.mail import send_mail

from . models import Token
import uuid


def index(request):
    return render(request, 'pages/index.html')

def register(request):
    if request.method == "GET":
        return render(request, 'pages/register.html')
    if request.method == "POST":
        user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
        token = Token.objects.create(user=user, body=uuid.uuid4())
        send_mail(
            'Your registration is complete!',
            f'Your registration is complete! Your invite link: localhost:8000/login/token/{token.body}',
            'admin@admin.com',
            [user.email],
        )
        return redirect("/")

def send_login_link(request):
    if request.method == "GET":
        return render(request, "pages/login.html")

    if request.method == "POST":
        user = User.objects.get(email=request.POST["email"])
        # return HttpResponse(user)
        token = user.token.body
        send_mail(
            'Login link',
            f'Your login link: localhost:8000/login/token/{token}',
            'admin@admin.com',
            [user.email],
        )
        return redirect("/")

def login_with_token(request, token):
    if request.method == "GET":
        try:
            token = Token.objects.get(body=token)
            user = User.objects.get(pk=token.user.id)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth.login(request, user)

            if user.is_authenticated:
                return redirect("/")
            else:
                return HttpResponse("login-failed")

        except Token.DoesNotExist:
            return HttpResponse("wrong link")

def logout(request):
    auth.logout(request)
    return redirect('/')

from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from . models import Token
import uuid
from config import settings

def index(request):
    tokens = Token.objects.all()
    return render(request, 'pages/index.html', { 'tokens': tokens })

def register(request):
    if request.method == "GET":
        return render(request, 'pages/register.html')
    if request.method == "POST":
        user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
        token = Token.objects.create(user=user, body=uuid.uuid4())
        send_mail(
            'Your registration is complete!',
            f'Your registration is complete! Your invite link: 168.62.180.202/login/token/{token.body}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect("/")

def send_login_link(request):
    if request.method == "GET":
        return render(request, "pages/login.html")

    if request.method == "POST":
        user = User.objects.get(email=request.POST["email"])
        token = user.token.body
        send_mail(
            'Login link',
            f'Your login link: 168.62.180.202/login/token/{token}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect("/")

def login_with_token(request, token):
    if request.method == "GET":
        try:
            token = Token.objects.get(body=token)
            token.view_count += 1
            token.save()

            user = User.objects.get(pk=token.user.id)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth.login(request, user)

            if user.is_authenticated:
                return redirect("/")
            else:
                return HttpResponse("Login Failed")

        except Token.DoesNotExist:
            return HttpResponse("Something Is Wrong With Link")

def logout(request):
    auth.logout(request)
    return redirect('/')

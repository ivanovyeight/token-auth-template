from django.contrib.auth.models import User, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages
from config import settings
from . models import Token
import uuid

def index(request):
    tokens = Token.objects.all()
    return render(request, 'pages/index.html', { 'tokens': tokens })

def register(request):
    if request.method == "GET":
        return render(request, 'pages/register.html')
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST["email"])
            user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
            token = Token.objects.create(user=user, body=uuid.uuid4())
            send_mail(
                'Your registration is complete!',
                f'Your registration is complete! Your invite link: https://tokenauth.ivanovyeight.club/login/token/{token.body}',
                # f'Your login link: http://localhost:8000/login/token/{token.body}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            messages.info(request, "Welcome! You'll receive email with invite link within 5 minutes!")
            return redirect("/")
        except:
            messages.info(request, "This email is already registered.")
            return redirect("/")

def send_login_link(request):
    if request.method == "GET":
        return render(request, "pages/login.html")

    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST["email"])
            token = user.token.body
            send_mail(
                'Login link',
                f'Your login link: https://tokenauth.ivanovyeight.club/login/token/{token}',
                # f'Your login link: http://localhost:8000/login/token/{token}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            messages.info(request, "Welcome back! You'll receive email with invite link within 5 minutes!")
            return redirect("/")
        except:
            messages.info(request, "User Not Found.")
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
                messages.info(request, f"Welcome back, {user.username}!")
                return redirect("/")
            else:
                return HttpResponse("Login Failed")
        except:
            messages.info(request, "Something Is Wrown With Provided Link. Try Again.")
            return redirect("/")

def logout(request):
    auth.logout(request)
    return redirect('/')

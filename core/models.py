from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    body = models.CharField(max_length=36, unique=True)
    view_count = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
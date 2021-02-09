from django.contrib import admin
from . models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = ['body', 'view_count', 'user']
    list_display_links = ['body', 'user']

admin.site.register(Token, TokenAdmin)

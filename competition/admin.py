from django.contrib import admin
from .models import LandingPage
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(LandingPage, MarkdownxModelAdmin)

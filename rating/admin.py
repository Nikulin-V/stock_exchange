from django.contrib import admin

from .models import *


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'points')

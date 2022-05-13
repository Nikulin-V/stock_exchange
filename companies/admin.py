from django.contrib import admin

from .models import *


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry')
    list_display_links = ('name',)

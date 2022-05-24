from django.contrib import admin

from .models import Lot, Shares


@admin.register(Shares)
class SharesAdmin(admin.ModelAdmin):
    list_display = ('company', 'count', 'user')


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('company', 'count', 'price', 'user')

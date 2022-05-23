from django.contrib import admin

from .models import *


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


class GalleryInlined(admin.TabularInline):
    model = Photo
    can_delete = False
    readonly_fields = ('image',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'industry',
        'is_active',
        'image_tmb',
    )
    list_editable = ('is_active',)
    list_display_links = ('name',)
    exclude = ('gallery',)
    inlines = (GalleryInlined,)

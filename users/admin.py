from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile

User = get_user_model()


class ProfileInlined(admin.TabularInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Кошелёк', {'fields': ('balance', 'trust_points')}),
    )
    list_display = ('username', 'email', 'balance', 'is_staff')
    list_editable = ('balance',)
    inlines = (ProfileInlined,)


admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class ProfileInlined(admin.TabularInline):
    model = Profile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'balance', 'is_staff')
    list_editable = ('balance',)
    exclude = ('password', 'last_login', 'date_joined', 'is_superuser', 'groups', 'user_permissions')
    inlines = (ProfileInlined,)


admin.site.register(User, UserAdmin)

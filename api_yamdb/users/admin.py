from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'role']
    exclude = ('groups', 'user_permissions', 'password', 'last_login')


admin.site.register(User, CustomUserAdmin)

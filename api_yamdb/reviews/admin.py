from django.contrib import admin

from .models import Comment, Review, Title, User


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'role']
    exclude = ('groups', 'user_permissions', 'password', 'last_login')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)

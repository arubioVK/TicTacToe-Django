from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.models import User


class UserExtendsAdmin(UserAdmin):
    list_display = ("username", "email", "is_active",)
    fieldsets = (
        (None, {"fields": ("username","email", "password")}),
        ("Permissions", {"fields": ("email_verified","is_active","is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    ordering = ("username",)
    
admin.site.register(User, UserExtendsAdmin)
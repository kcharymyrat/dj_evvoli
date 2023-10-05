from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ["username", "email", "id"]
    ordering = ["-is_superuser", "-is_staff", "username"]


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)


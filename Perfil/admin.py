from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Direccion

# Register your models here.
user = get_user_model()

class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "password",
                    ("username", "email"),
                    ("first_name", "last_name"),
                    "imagen",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": [
                    "groups",
                    "user_permissions",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "last_login",
                    "date_joined",
                ],
            },
        ),
    ]


admin.site.register(user, CustomUserAdmin)
admin.site.register(Direccion)


# "fields": ["password", ("username", "email"), ("first_name", "last_name"), "imagen"],

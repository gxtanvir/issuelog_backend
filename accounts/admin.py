from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, Module


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("user_id", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("user_id", "name", "password")}),
        # ("Profile Info", {"fields": ("companies", "modules")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
        ("Custom Fields", {"fields": ("companies", "modules")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("user_id", "name", "password1", "password2", "companies", "modules", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("user_id", "name")
    ordering = ("user_id",)
    filter_horizontal = ("companies", "modules", "groups", "user_permissions")


admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(Module)

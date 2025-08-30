from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User

# Choices for companies and modules (adjust as needed)
COMPANY_CHOICES = [
    ("GMS Composite", "GMS Composite"),
    ("GMS Textile", "GMS Textile"),
    ("GMS Trims", "GMS Trims"),
    ("GMS Testing Laboratory", "GMS Testing Laboratory")
]

MODULE_CHOICES = [
    ("MM", "MM"),
    ("TNA", "TNA"),
    ("Plan", "Plan"),
    ("Commercial", "Commercial"),
    ("SCM", "SCM"),
    ("Inventory", "Inventory"),
    ("Prod", "Prod"),
    ("S. Com", "S. Con"),
    ("Printing", "Printing"),
    ("AOP", "AOP"),
    ("Wash", "Wash"),
    ("Embroidery", "Embroidery"),
    ("Laboratory", "Laboratory")
]

# Custom form for creating and updating users
class UserAdminForm(forms.ModelForm):
    # Use MultipleChoiceField for list fields
    companies = forms.MultipleChoiceField(
        choices=COMPANY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    modules = forms.MultipleChoiceField(
        choices=MODULE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate form fields from JSONField lists
        if self.instance and self.instance.pk:
            self.fields["companies"].initial = self.instance.companies
            self.fields["modules"].initial = self.instance.modules

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Save the selected choices as lists in JSONField
        instance.companies = self.cleaned_data.get("companies", [])
        instance.modules = self.cleaned_data.get("modules", [])
        if commit:
            instance.save()
        return instance

class UserAdmin(BaseUserAdmin):
    form = UserAdminForm

    list_display = (
        "user_id",
        "name",
        "display_companies",
        "display_modules",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("user_id", "name", "password")}),
        ("Profile Info", {"fields": ("companies", "modules")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
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
    filter_horizontal = ("groups", "user_permissions")

    # Display JSONField lists
    def display_companies(self, obj):
        return ", ".join(obj.companies) if obj.companies else "-"
    display_companies.short_description = "Companies"

    def display_modules(self, obj):
        return ", ".join(obj.modules) if obj.modules else "-"
    display_modules.short_description = "Modules"

# Register the custom User model
admin.site.register(User, UserAdmin)

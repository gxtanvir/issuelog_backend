from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("issue_id", "company_name", "priority", "responsible_party", "gms_status", "inserted_by_name", "issue_raise_date")
    list_filter = ("company_name", "priority", "responsible_party", "gms_status")
    search_fields = ("issue_details", "company_name", "raised_by", "responsible_person", "inserted_by_name")

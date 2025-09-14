from django.db import models
from django.conf import settings

PRIORITY_CHOICES = [
    ("High", "High"),
    ("Medium", "Medium"),
    ("Regular", "Regular"),
]

MODULE_CHOICES = [
    ("MM", "MM"), ("TNA", "TNA"), ("Plan", "Plan"), ("Commercial", "Commercial"),
    ("SCM", "SCM"), ("Inventory", "Inventory"), ("Prod", "Prod"),
    ("S.Con", "S.Con"), ("Printing", "Printing"), ("AOP", "AOP"),
    ("Wash", "Wash"), ("Embroidery", "Embroidery"), ("Laboratory", "Laboratory"),
]

VIA_CHOICES = [
    ("Phone", "Phone"), ("Email", "Email"), ("Direct", "Direct"),
]

RESP_PARTY_CHOICES = [
    ("Logic", "Logic"), ("MIS", "MIS"),
]

STATUS_CHOICES = [
    ("Pending", "Pending"), ("Done", "Done"),
]

class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    raised_by = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    module = models.CharField(max_length=50, blank=True)
    via = models.CharField(max_length=20, choices=VIA_CHOICES)
    issue_details = models.TextField()
    responsible_party = models.CharField(max_length=10, choices=RESP_PARTY_CHOICES)
    responsible_person = models.CharField(max_length=100, null=True, blank=True)
    gms_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    issue_raise_date = models.DateField()
    deadline = models.DateField(null=True, blank=True)
    complete_date = models.DateField(null=True, blank=True)
    comment_date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    # User who inserted the issue
    inserted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inserted_issues"
    )
    inserted_by_name = models.CharField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.inserted_by and not self.inserted_by_name:
            self.inserted_by_name = self.inserted_by.get_username()
        if self.responsible_party == "MIS" and not self.responsible_person and self.inserted_by:
            self.responsible_person = self.inserted_by.get_username()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Issue {self.issue_id} - {self.company_name}"

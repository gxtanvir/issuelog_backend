from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["inserted_by", "inserted_by_name", "created_at", "issue_id", "updated_at"]

    # Accept empty strings as null for optional fields
    def to_internal_value(self, data):
        for k in ["deadline", "complete_date", "comment_date", "comments", "responsible_person", "module"]:
            if data.get(k) in ["", None]:
                data[k] = None
        return super().to_internal_value(data)
    
    def validate(self, data):
        deadline = data.get("deadline")
        crm = data.get("crm")

        if deadline and not crm:
            raise serializers.ValidationError(
                {"crm": "CRM is required if deadline is set."}
            )
        return data

    # create: set inserted_by from request, fill MIS responsible_person if missing
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['inserted_by'] = user
        if validated_data.get("responsible_party") == "MIS" and not validated_data.get("responsible_person"):
            validated_data["responsible_person"] = user.name  # use display name
        return super().create(validated_data)

    # update: same MIS autofill logic
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if validated_data.get("responsible_party") == "MIS" and not validated_data.get("responsible_person"):
            validated_data["responsible_person"] = user.name
        return super().update(instance, validated_data)

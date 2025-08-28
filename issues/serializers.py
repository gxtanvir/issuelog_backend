from rest_framework import serializers
from .models import Issue
from accounts.models import User 

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["inserted_by", "inserted_by_name", "created_at", "issue_id"]

    # Accept empty strings as null for optional fields
    def to_internal_value(self, data):
        for k in ["deadline", "complete_date", "comment_date", "comments", "responsible_person", "module"]:
            if data.get(k) in ["", None]:
                data[k] = None
        return super().to_internal_value(data)

    # Automatically set inserted_by from logged-in user
    def create(self, validated_data):
        user = self.context['request'].user  # logged-in user
        validated_data['inserted_by'] = user

        # If MIS and responsible_person missing, fill with username
        if validated_data.get("responsible_party") == "MIS" and not validated_data.get("responsible_person"):
            validated_data["responsible_person"] = user.get_username()

        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id", "name", "company_name", "modules", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

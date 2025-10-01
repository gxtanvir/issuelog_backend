from rest_framework import serializers
from .models import User, Company, Module


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    companies = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), many=True
    )
    modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), many=True
    )

    class Meta:
        model = User
        fields = ["id", "user_id", "name", "email", "password", "companies", "modules", "is_staff",
            "is_superuser", ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        companies = validated_data.pop("companies", [])
        modules = validated_data.pop("modules", [])
        password = validated_data.pop("password", None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # assign companies & modules
        user.companies.set(companies)
        user.modules.set(modules)
        return user

    def update(self, instance, validated_data):
        companies = validated_data.pop("companies", None)
        modules = validated_data.pop("modules", None)

        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        if companies is not None:
            instance.companies.set(companies)
        if modules is not None:
            instance.modules.set(modules)

        return instance

class UserSignupSerializer(serializers.ModelSerializer):
    companies = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), many=True
    )
    modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), many=True
    )

    class Meta:
        model = User
        fields = ["user_id", "name", "email", "password", "companies", "modules",
            "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        companies = validated_data.pop("companies", [])
        modules = validated_data.pop("modules", [])
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)
        user.companies.set(companies)
        user.modules.set(modules)
        return user
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField()

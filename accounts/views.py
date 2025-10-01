from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company, Module
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.core.mail import send_mail
from .models import User, PasswordResetCode
from.serializers import PasswordResetRequestSerializer, PasswordVerifyCodeSerializer, PasswordResetConfirmSerializer
from .serializers import (
    UserSerializer,
    CompanySerializer,
    ModuleSerializer,
    UserSignupSerializer,
)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class ModuleListView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "companies": [c.name for c in user.companies.all()],
        "modules": [m.name for m in user.modules.all()],
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        # IMPORTANT: here must match your USERNAME_FIELD
        user = authenticate(username=user_id, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            # add admin flags to response
            user_data["is_staff"] = user.is_staff
            user_data["is_superuser"] = user.is_superuser

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)

        # generate and save code
        code = PasswordResetCode.generate_code()
        PasswordResetCode.objects.create(user=user, code=code)

        # send email
        send_mail(
            "Your Password Reset Code",
            f"Use this code to reset your password: {code}\n(valid for 10 minutes)",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return Response({"success": "Reset code sent to email"}, status=status.HTTP_200_OK)


class PasswordVerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordVerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_obj = PasswordResetCode.objects.filter(user=user, code=code).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if reset_obj.is_expired():
            return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Code is valid"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_obj = PasswordResetCode.objects.filter(user=user, code=code).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if reset_obj.is_expired():
            return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"success": "Password reset successfully"}, status=status.HTTP_200_OK)

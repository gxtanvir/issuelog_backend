from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

# Register API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

# Login API (JWT)
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

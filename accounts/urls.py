from django.urls import path
from .views import RegisterView, LoginView
from django.http import JsonResponse

def accounts_home(request):
    return JsonResponse({"message": "Accounts API is working 🚀"})

urlpatterns = [
     path("", accounts_home, name="accounts_home"), 
     path('register/', RegisterView.as_view(), name="register"),
     path('login/', LoginView.as_view(), name="login"),
]

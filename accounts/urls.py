from django.urls import path
from .views import RegisterView, LoginView, CompanyListView, ModuleListView, me
from django.http import JsonResponse

def accounts_home(request):
    return JsonResponse({"message": "Accounts API is working 🚀"})

urlpatterns = [
     path("", accounts_home, name="accounts_home"), 
     path('register/', RegisterView.as_view(), name="register"),
     path('login/', LoginView.as_view(), name="login"),
     path("companies/", CompanyListView.as_view(), name="company-list"),
    path("modules/", ModuleListView.as_view(), name="module-list"),
    path("me/", me, name="me"),
]

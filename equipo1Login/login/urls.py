from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegistroView.as_view(), name="users-register"),
    path("login/", views.MiTokenObtainPairView.as_view(), name="users-login"),
    path("<int:pk>/profile/", views.PerfilUsuarioView.as_view(), name="users-profile"),
]

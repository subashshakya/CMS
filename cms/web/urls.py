from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("user-signup/", views.user_signup, name="user-signup"),
    path("user-signin/", views.user_sign_in, name="user-signin"),
]

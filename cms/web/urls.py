from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("user-signup", views.user_signup, name="user-signup"),
    path("user-signin", views.user_sign_in, name="user-signin"),
    path("service", views.service, name="service-post"),
    path("service/<int:id>", views.service, name="service-RUD"),
    path("personel", views.personel, name="personel create"),
    path("personel/<int:id>", views.personel, name="personel RUD"),
]

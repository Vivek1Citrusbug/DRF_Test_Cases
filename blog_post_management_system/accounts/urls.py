from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    RegistrationView,
    CustomLoginView,
)

urlpatterns = [
    # path("",views.home_page,name = ""),
    path("registration/", RegistrationView.as_view(), name="user-registration"),
    path("login/", CustomLoginView.as_view(), name="user-login"),
    path("logout/", views.logout_view, name="user-logout"),
    path("blogs/", include("blogs.urls"), name="blogs"),
    path("userprofile/", ProfileDetailView.as_view(), name="profile"),
    path("userprofile/edit", ProfileUpdateView.as_view(), name="profile_edit"),
]


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("splash", views.splash, name="splash"),
    path("movie/<int:movid>", views.movie, name="movie"),
    path("search", views.search, name="search"),
    path("profile", views.profile, name="profile"),
    path("profile/<str:parameter>", views.profile, name="profile"),
    path("getservices", views.services, name="services"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]

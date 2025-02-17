from django.urls import path

from Bookmanagement.views import Login, Signup

urlpatterns = [
    path("signup/", Signup.as_view()),
    path("login/", Login.as_view()),
]
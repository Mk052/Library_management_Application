from django.urls import path

from Bookmanagement.views import Signup

urlpatterns = [
    path("signup/", Signup.as_view()),
]

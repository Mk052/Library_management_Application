from django.urls import path

from Bookmanagement.views import Login, Logout, Signup, AuthorAPIView

urlpatterns = [
    path("signup/", Signup.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("author/", AuthorAPIView.as_view()),
    path("author/<int:pk>/", AuthorAPIView.as_view()),
]

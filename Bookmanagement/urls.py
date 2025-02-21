from django.urls import path

from Bookmanagement.views import (
    AuthorAPIView,
    BookAPIView,
    CategoryAPIView,
    CourseAPIView,
    IssueBookAPIView,
    Login,
    Logout,
    Signup,
    StudentAPIView,
)

urlpatterns = [
    path("signup/", Signup.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("author/", AuthorAPIView.as_view()),
    path("author/<int:pk>/", AuthorAPIView.as_view()),
    path("category/", CategoryAPIView.as_view()),
    path("category/<int:pk>/", CategoryAPIView.as_view()),
    path("course/", CourseAPIView.as_view()),
    path("course/<int:pk>/", CourseAPIView.as_view()),
    path("student/", StudentAPIView.as_view()),
    path("student/<int:pk>/", StudentAPIView.as_view()),
    path("book/", BookAPIView.as_view()),
    path("book/<int:pk>/", BookAPIView.as_view()),
    path("issuebook/", IssueBookAPIView.as_view()),
]

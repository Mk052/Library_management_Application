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
    ReturnBookAPIView,
    FineAPIView,
    StudentFineAPIView
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
    path("issuebook/<int:pk>/", IssueBookAPIView.as_view()),
    path("returnbook/<int:pk>/", ReturnBookAPIView.as_view()),
    path("fine/", FineAPIView.as_view()),
    path("fine/<int:pk>/", FineAPIView.as_view()),
    path("studentfine/", StudentFineAPIView.as_view()),
]

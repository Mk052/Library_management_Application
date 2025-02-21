from django.contrib.auth.models import AbstractUser
from django.db import models

from Bookmanagement.manager import CustomUserManager


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Avoid Creating a Separate Database Table


class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(TimestampedModel):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return self.name


class Book(TimestampedModel):
    title = models.CharField(max_length=100)
    Description = models.TextField(blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    is_avaliable = models.BooleanField(default=True)
    total_book = models.PositiveIntegerField(default=1)
    book_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Course(TimestampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(AbstractUser, TimestampedModel):
    username = None
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    roll_no = models.PositiveIntegerField(unique=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class IssueBook(TimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issuebook")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="issuebook", blank=True
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} Book issued to {self.student.email}"


class Fine(TimestampedModel):
    issue_book = models.ForeignKey(
        IssueBook, on_delete=models.CASCADE, related_name="fines"
    )
    amount = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.issue_book}"

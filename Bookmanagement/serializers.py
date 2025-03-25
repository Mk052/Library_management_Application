from rest_framework import serializers

from Bookmanagement.models import (
    Author,
    Book,
    Category,
    Course,
    Fine,
    IssueBook,
    Student,
)

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    course = serializers.StringRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="course",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "email",
            "password",
            "roll_no",
            "course",
            "course_id",
        ]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "bio"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "Description",
            "author",
            "category",
            "is_avaliable",
            "book_copies",
            "author_id",
            "category_id",
        ]


class IssueBookSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    student = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = IssueBook
        fields = [
            "id",
            "book",
            "student",
            "issue_date",
            "return_date",
            "is_returned",
            "book_id",
            "student_id",
        ]


class FineSerializer(serializers.ModelSerializer):
    issue_book_id = serializers.PrimaryKeyRelatedField(
        queryset=IssueBook.objects.all(), source="issue_book", write_only=True
    )
    issue_book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Fine
        fields = ["id", "issue_book", "amount", "paid", "issue_book_id"]

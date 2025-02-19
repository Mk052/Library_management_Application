from rest_framework import serializers

from Bookmanagement.models import Author, Category, Course, Student


class StudentSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    course = serializers.StringRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
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


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "bio"]


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class CourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ["name"]

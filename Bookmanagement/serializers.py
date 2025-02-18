from rest_framework import serializers

from Bookmanagement.models import Student, Author


class StudentSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["id", "full_name", "email", "password", "roll_no"]


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "bio"]

from rest_framework import serializers

from Bookmanagement.models import Student


class StudentSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["id", "full_name", "email", "password", "roll_no"]

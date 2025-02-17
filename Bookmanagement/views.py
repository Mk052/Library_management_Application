from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Bookmanagement.models import Student
from Bookmanagement.serializers import StudentSerializers


class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializers = StudentSerializers(data=request.data)
        password = request.data.get("password")
        if serializers.is_valid():
            user = serializers.save()
            user.set_password(password)
            user.save()
            return Response(
                {"msg": "created student", "data": serializers.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializers.errors)
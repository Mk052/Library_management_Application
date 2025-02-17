from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = Student.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)}
            )
        else:
            return Response(
                {"msg": "Student Does not exits"}, status=status.HTTP_401_UNAUTHORIZED
            )
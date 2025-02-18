from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Bookmanagement.models import Author, Student
from Bookmanagement.pagination import CustomPagination
from Bookmanagement.serializers import AuthorSerializers, StudentSerializers


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


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Successfully logout"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "invalid user or other error"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# **************************** Author Management start *******************


class AuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = AuthorSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                {"msg": "Created the Author"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            data = Author.objects.filter(id=pk).first()
            serializer = AuthorSerializers(data)
            if data:
                return Response(
                    {"msg": "retrieve the author", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "Author does not Exits"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = Author.objects.all()
            paginator = CustomPagination()
            paginator_author = paginator.paginate_queryset(
                data, request
            )  # Gets a small part of the authors list based on the page number in the request.
            serializer = AuthorSerializers(paginator_author, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# ******************************* Author Management end ***********************

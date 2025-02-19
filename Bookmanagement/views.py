from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Bookmanagement.models import Author, Book, Category, Course, Student
from Bookmanagement.pagination import CustomPagination
from Bookmanagement.permissions import CustomPermission
from Bookmanagement.serializers import (
    AuthorSerializers,
    CategorySerializers,
    CourseSerializers,
    StudentSerializers,
)


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

    def put(self, request, pk=None):
        if pk:
            id = pk
            author = Author.objects.filter(id=id).first()
            if author:
                serializer = AuthorSerializers(author, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"msg": "completed data updated", "data": serializer.data},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"msg": "author does not exists"}, status=status.HTTP_404_NOT_FOUND
                )

    def patch(self, request, pk=None):
        if pk:
            id = pk
            author = Author.objects.filter(id=id).first()
            if author:
                serializer = AuthorSerializers(author, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"msg": "partial data updated", "data": serializer.data},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"msg": "author does not exists"}, status=status.HTTP_404_NOT_FOUND
                )

    def delete(self, request, pk=None):
        if pk:
            id = pk
            author = Author.objects.filter(id=id).first()
            if author:
                author.delete()
                return Response(
                    {"msg": "Successfully deleted the author"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "author does not exist"}, status=status.HTTP_404_NOT_FOUND
                )


# ******************************* Author Management end ***********************
# ****************************** Category Management start ********************
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Successfully Created a category", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            id = pk
            category = Category.objects.filter(id=id).first()
            if category:
                serializer = CategorySerializers(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "category does not exits"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            category = Category.objects.all()
            paginator = CustomPagination()
            paginator_category = paginator.paginate_queryset(category, request)
            serializer = CategorySerializers(paginator_category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        category = Category.objects.filter(id=pk).first()
        if category:
            serializer = CategorySerializers(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Successfully update the data", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"msg": "Category does not exits"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk=None):
        category = Category.objects.filter(id=pk).first()
        if category:
            category.delete()
            return Response(
                {"msg": "Successfully deleted the category"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"msg": "category does not exits"}, status=status.HTTP_404_NOT_FOUND
            )


# ****************************** Category Management end ********************
# ****************************** Course Management start ********************
class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Successfully Created a course", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            course = Course.objects.filter(id=pk).first()
            if course:
                serializer = CourseSerializers(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "course does not exits"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            course = Course.objects.all()
            paginator = CustomPagination()
            paginator_course = paginator.paginate_queryset(course, request)
            serializer = CourseSerializers(paginator_course, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        course = Course.objects.filter(id=pk).first()
        if course:
            serializer = CourseSerializers(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Successfully update the data", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"msg": "Course does not exits"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk=None):
        course = Course.objects.filter(id=pk).first()
        if course:
            course.delete()
            return Response(
                {"msg": "Successfully deleted the course"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"msg": "course does not exits"}, status=status.HTTP_404_NOT_FOUND
            )


# ****************************** Course Management end ********************

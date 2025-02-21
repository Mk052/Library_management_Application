from django.db.models import Q
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Bookmanagement.models import (
    Author,
    Book,
    Category,
    Course,
    Fine,
    IssueBook,
    Student,
)
from Bookmanagement.pagination import CustomPagination
from Bookmanagement.permissions import CustomPermission
from Bookmanagement.serializers import (
    AuthorSerializer,
    BookSerializer,
    CategorySerializer,
    CourseSerializer,
    FineSerializer,
    IssueBookSerializer,
    StudentSerializer,
)


class Signup(APIView):

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(
            {"msg": "created student", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class Login(APIView):

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
        serializers = AuthorSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"msg": "Created the Author"}, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        if pk:
            data = Author.objects.filter(id=pk).first()
            serializer = AuthorSerializer(data)
            if not data:
                return Response(
                    {"msg": "Author does not Exits"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"msg": "retrieve the author", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        else:
            data = Author.objects.all()
            paginator = CustomPagination()
            paginator_author = paginator.paginate_queryset(
                data, request
            )  # Gets a small part of the authors list based on the page number in the request.
            serializer = AuthorSerializer(paginator_author, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):

        if not pk:
            return Response(
                {"msg": "ID is required!"}, status=status.HTTP_400_BAD_REQUEST
            )

        author = Author.objects.filter(id=pk).first()

        if not author:
            return Response(
                {"msg": "author does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AuthorSerializer(author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "completed data updated", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk=None):
        author = Author.objects.filter(id=pk).first()
        if not author:
            return Response(
                {"msg": "author does not exists"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "partial data updated", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        author = Author.objects.filter(id=pk).first()
        if not author:
            return Response(
                {"msg": "author does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        author.delete()
        return Response(
            {"msg": "Successfully deleted the author"},
            status=status.HTTP_200_OK,
        )


# ******************************* Author Management end ***********************
# ****************************** Category Management start ********************


class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully Created a category", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, pk=None):
        if pk:
            category = Category.objects.filter(id=pk).first()
            if category:
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "category does not exits"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            category = Category.objects.all()
            paginator = CustomPagination()
            paginator_category = paginator.paginate_queryset(category, request)
            serializer = CategorySerializer(paginator_category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        category = Category.objects.filter(id=pk).first()
        if not category:
            return Response(
                {"msg": "Category does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully update the data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        category = Category.objects.filter(id=pk).first()
        if not category:
            return Response(
                {"msg": "category does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response(
            {"msg": "Successfully deleted the category"},
            status=status.HTTP_204_NO_CONTENT,
        )


# ****************************** Category Management end ********************
# ****************************** Course Management start ********************


class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully Created a course", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, pk=None):
        if pk:
            course = Course.objects.filter(id=pk).first()
            if course:
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "course does not exits"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            course = Course.objects.all()
            paginator = CustomPagination()
            paginator_course = paginator.paginate_queryset(course, request)
            serializer = CourseSerializer(paginator_course, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        course = Course.objects.filter(id=pk).first()
        if not course:
            return Response(
                {"msg": "Course does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully update the data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        course = Course.objects.filter(id=pk).first()
        if not course:
            return Response(
                {"msg": "course does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        course.delete()
        return Response(
            {"msg": "Successfully deleted the course"},
            status=status.HTTP_204_NO_CONTENT,
        )


# ****************************** Course Management end ********************
# ****************************** Student Management start ********************


class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            student = Student.objects.filter(id=pk).first()
            if not student:
                return Response(
                    {"msg": "Student does not exits"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            student = Student.objects.all()
            paginator = CustomPagination()
            paginator_student = paginator.paginate_queryset(student, request)
            serializer = StudentSerializer(paginator_student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        student = Student.objects.filter(id=pk).first()
        if not student:
            return Response(
                {"msg": "Student does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully update the student data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# ****************************** Student Management end ********************
# ****************************** Book Management start ********************


class BookAPIView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully create the Book", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, pk=None):
        author = request.GET.get("author")
        category = request.GET.get("category")
        if pk:
            book = Book.objects.filter(id=pk).first()
            if not book:
                return Response(
                    {"msg": "Book does not exit"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)

        book = Book.objects.all()
        if author:
            book = book.filter(author__name=author)
        if category:
            book = book.filter(category__name=category)
        paginator = CustomPagination()
        paginator_book = paginator.paginate_queryset(book, request)
        serializer = BookSerializer(paginator_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return Response(
                {"msg": "Book does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully update the Book data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return Response({"msg": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(
            {"msg": "Successfully delete the Book"}, status=status.HTTP_204_NO_CONTENT
        )


# ****************************** Book Management end ********************
# ****************************** IssueBook Management start ******************


class IssueBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get("book_id")
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({"msg": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        if not (book.is_avaliable and book.book_copies > 1):
            return Response({"msg": "Book is not avaliable"}, status=status.HTTP_200_OK)
        book.book_copies -= 1
        book.save()
        serializer = IssueBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user)
        return Response(
            {"msg": "Successfully the issue Book", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        student = request.GET.get("student")
        book = request.GET.get("book")
        issue_book = IssueBook.objects.all()
        if student:
            issue_book = issue_book.filter(student__name=student)
        if book:
            issue_book = issue_book.filter(book__name=book)
        paginator = CustomPagination()
        paginator_issuebook = paginator.paginate_queryset(issue_book, request)
        serializer = IssueBookSerializer(paginator_issuebook, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        issue_book = IssueBook.objects.filter(id=pk).first()
        if not issue_book:
            return Response({"msg": "book not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != issue_book.student:
            return Response(
                {"msg": "you are not authorized to return the book"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if issue_book.is_returned:
            return Response({"msg": "you already returned the book"})
        issue_book.is_returned = True
        issue_book.return_date = now()
        issue_book.save()
        book = issue_book.book
        book.book_copies += 1
        book.save()
        serializer = IssueBookSerializer(issue_book)
        return Response(
            {"msg": "Successfully returned the book", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


# ****************************** IssueBook Management end ********************
# ****************************** Fine Management start ********************
class FineAPIView(APIView):

    def post(self, request):
        serializer = FineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully created the Fine", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, pk=None):
        if pk:
            fine = Fine.objects.filter(issue_book__id=pk).first()
            if not fine:
                return Response(
                    {"msg": "fine does not exit"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = FineSerializer(fine)
            return Response(serializer.data, status=status.HTTP_200_OK)

        fine = Fine.objects.all()
        paginator = CustomPagination()
        paginator_fine = paginator.paginate_queryset(fine, request)
        serializer = FineSerializer(paginator_fine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        fine = Fine.objects.filter(id=pk).filter()
        if not fine:
            return Response(
                {"msg": "fine does not exit"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = FineSerializer(fine, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "Successfully update the data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk=None):
        fine = Fine.objects.filter(id=pk).filter()
        if not fine:
            return Response(
                {"msg": "fine does not exit"}, status=status.HTTP_404_NOT_FOUND
            )
        # if request.user != fine.issue_book.student:
        #     return Response({"msg": "you are not authorized to pay the fine"},
        #                     status=status.HTTP_403_FORBIDDEN)
        fine.paid = True
        fine.save()
        serializer = FineSerializer(fine)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(
            {"msg": "Successfully partially updated the data", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        fine = Fine.objects.filter(id=pk).first()
        if not fine:
            return Response(
                {"msg": "fine does not exit"}, status=status.HTTP_404_NOT_FOUND
            )

        fine.delete()
        return Response(
            {"msg": "Successfully delete the fine"}, status=status.HTTP_204_NO_CONTENT
        )


class StudentFineAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user
        issue_books = IssueBook.objects.filter(student=student)
        fine = Fine.objects.filter(issue_book__in=issue_books)
        paginator = CustomPagination()
        paginator_fine = paginator.paginate_queryset(fine, request)
        serializer = FineSerializer(paginator_fine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ****************************** Fine Management end ********************

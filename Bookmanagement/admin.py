from django.contrib import admin
from Bookmanagement.models import IssueBook, Fine 


@admin.register(IssueBook)
class IssueBookAdmin(admin.ModelAdmin):
    list_display = ["id", "book", "student", "is_returned", "issue_date", "return_date"]


@admin.register(Fine)
class FineBookAdmin(admin.ModelAdmin):
    list_display = ["id", "issue_book", "amount"]
import datetime

from django.http import JsonResponse, HttpRequest
# Create your views here.
from django.views import View
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book


def check_unique_title(value):
    print(f'value is: {value}')
    if Book.objects.filter(title=value).exists():
        raise ValidationError('title must be unique')


def check_min_length(value):
    if len(value) < 3:
        raise ValidationError('title length must be more than 3')


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=True, validators=[check_unique_title, check_min_length])
    author_id = serializers.IntegerField(default=1)
    id = serializers.IntegerField(read_only=True)
    published_date = serializers.DateField(allow_null=True, required=False, initial='2022-10-10')

    def validate_title(self, value):
        check_unique_title(value)
        if len(value) > 10:
            raise ValidationError("title must be less than 10 chars")
        value = value.lower()
        return value

    def validate_published_date(self, value):
        if datetime.datetime.strptime(value, '%Y-%M-%d') > datetime.datetime.now():
            raise ValidationError("published date must be less than current time")


class BookView(View):
    def get(self, request: HttpRequest):
        return JsonResponse({'name': None}, safe=False)


class BookApiView(APIView):
    """
    My Book API view
    """

    def get(self, request: Request):
        book = Book.objects.get(id=1)
        book_serializer = BookSerializer(book)
        return Response(book_serializer.data)

    def post(self, request):
        book_serializer = BookSerializer(data=request.data)
        book_serializer.is_valid(raise_exception=True)
        print('request data was valid')
        return Response(book_serializer.data)

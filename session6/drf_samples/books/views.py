from django.http import JsonResponse, HttpRequest
# Create your views here.
from django.views import View
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book, Comment
from books.serializers import BookSerializer, CommentSerializer


class BookView(View):
    def get(self, request: HttpRequest):
        return JsonResponse({'name': None}, safe=False)


class CommentListView(APIView):
    def get(self, request):
        serializer = CommentSerializer(Comment.objects.all(), many=True)
        return Response(serializer.data)


class BookApiView(APIView):
    """
    My Book API view
    """

    def get(self, request: Request, *args, **kwargs):
        book = Book.objects.get(id=kwargs['pk'])
        book_serializer = BookSerializer(book)
        return Response(book_serializer.data)

    def post(self, request, *args, **kwargs):
        book_serializer = BookSerializer(data=request.data)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save(something=True)
        print('request data was valid', book_serializer.validated_data['title'])
        return Response(book_serializer.data)

    def put(self, request, pk):
        book = Book.objects.get(id=pk)
        book_serializer = BookSerializer(data=request.data, instance=book)
        if book_serializer.is_valid(raise_exception=False):
            book = book_serializer.save()
            return Response(book_serializer.data)
        return Response(book_serializer.errors.data)

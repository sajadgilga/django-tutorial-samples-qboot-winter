import json

from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from post.utils import publish_post
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book, Comment
from books.serializers import CommentSerializer
from pagination_samples.settings import PAGINATION_DEFAULT_SIZE


def search_book(request):
    publish_post()
    query = request.GET.get('query', '')
    result = Book.objects.filter(title__contains=query).first()
    return HttpResponse(f"result for query {query} is: {result.description if result else 'nothing found'}")


class BookXSSView(View):
    def get(self, request):
        book = Book.objects.last()
        return render(request, 'books.html', context={
            'book': book
        })


@csrf_exempt
def collect_token(request):
    data = json.loads(request.body)
    print('collected data is: ', data)
    return JsonResponse({})


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()

        page_number = request.GET.get('page', 1)
        paginator = Paginator(books, PAGINATION_DEFAULT_SIZE)
        books_page = paginator.get_page(page_number)

        return render(request, 'book-list.html', context={'books': books_page})


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 40

    # max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'links': {
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
            },
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class BookListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    # throttle_classes = [AnonRateThrottle]

    def get_cache_key(self):
        return 'book-list-view-cache-key'

    def get(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        # result = cache.get(cache_key)
        # if result:
        #     return Response(result)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.all().select_related('book', 'user').prefetch_related('user__groups',
                                                                                     'user__user_permissions')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(self.get_cache_key(), serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(self.get_cache_key(), serializer.data, expires=5)
        return Response(serializer.data)


def check_scripts(text):
    if '<script>' in text:
        raise ValidationError('dangerous content')
    return text


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'tags']

    def clean_description(self):
        description = self.cleaned_data['description']
        description = check_scripts(description)


class BookCreateView(CreateView):
    template_name = 'book-form.html'
    form_class = BookCreateForm
    success_url = '/books/form-xss/'

    def get(self, request):
        self.object = Book.objects.last()
        return self.render_to_response(self.get_context_data())


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

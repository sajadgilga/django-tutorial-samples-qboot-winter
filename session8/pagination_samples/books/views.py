from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from books.models import Book, Comment
from books.serializers import CommentSerializer
from pagination_samples.settings import PAGINATION_DEFAULT_SIZE


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

    def get_cache_key(self):
        return 'book-list-view'

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
            # cache.set(self.get_cache_key(), serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # cache.set(self.get_cache_key(), serializer.data)
        return Response(serializer.data)

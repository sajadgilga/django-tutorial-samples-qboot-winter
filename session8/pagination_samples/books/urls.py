from django.urls import path

from books.views import BookListView, BookListApiView, search_book, BookXSSView, collect_token

urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list-view'),
    path('list-api/', BookListApiView.as_view(), name='book-list-api'),
    path('reflected-xss/', search_book),
    path('stored-xss/', BookXSSView.as_view()),
    path('collect-token/', collect_token),
]

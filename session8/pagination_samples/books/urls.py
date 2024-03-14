from django.urls import path

from books.views import BookListView, BookListApiView

urlpatterns = [
    path('list/', BookListView.as_view()),
    path('list-api/', BookListApiView.as_view()),
]

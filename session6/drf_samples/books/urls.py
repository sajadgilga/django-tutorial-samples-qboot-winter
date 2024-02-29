from django.urls import path

from books.views import BookView, BookApiView, CommentListView

urlpatterns = [
    path('django-book-view', BookView.as_view()),
    # path('drf-book-view', BookApiView.as_view()),
    path('<int:pk>/', BookApiView.as_view()),
    path('comments', CommentListView.as_view()),
]

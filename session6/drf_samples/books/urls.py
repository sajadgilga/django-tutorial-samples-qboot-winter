from django.urls import path

from books.views import BookView, BookApiView

urlpatterns = [
    path('django-book-view', BookView.as_view()),
    path('drf-book-view', BookApiView.as_view()),
    path('<int:pk>/info', BookApiView.as_view()),
]

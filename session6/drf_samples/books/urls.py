from django.urls import path
from rest_framework.routers import SimpleRouter

from books.views import BookView, BookApiView, CommentListView, BookViewset

router = SimpleRouter()

router.register('', BookViewset)

urlpatterns = [
                  path('django-book-view', BookView.as_view()),
                  # path('drf-book-view', BookApiView.as_view()),
                  path('<int:pk>/', BookApiView.as_view(), name='book-detail'),
                  path('comments', CommentListView.as_view()),
              ] + router.urls

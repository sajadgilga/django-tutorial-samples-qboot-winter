from django.urls import path
from rest_framework.routers import SimpleRouter

from books.views import BookView, BookApiView, CommentListView, BookViewset, CompanyViewSet

router = SimpleRouter()

router.register('books', BookViewset)
router.register('company', CompanyViewSet)

urlpatterns = [
                  path('django-book-view', BookView.as_view()),
                  # path('drf-book-view', BookApiView.as_view()),
                  path('<int:pk>/', BookApiView.as_view(), name='book-detail'),
                  path('comments', CommentListView.as_view()),
              ] + router.urls

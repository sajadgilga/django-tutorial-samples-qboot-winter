from .views import PostListView
from django.urls import path

urlpatterns = [
    path('list', PostListView.as_view(), name='post-list-view'),
]
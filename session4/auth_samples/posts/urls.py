from django.urls import path

from posts.views import PostEditView, PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_pk>/edit', PostEditView.as_view(), name='post_edit'),
]

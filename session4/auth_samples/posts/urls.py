from django.urls import path

from posts.views import PostEditView, PostDetailView, PostListView, PublishPostView, CreatePermissionView, \
    CreateGroupView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_pk>/edit', PostEditView.as_view(), name='post_edit'),
    path('<int:pk>/publish/', PublishPostView.as_view(), name='post_publish'),
    path('permissions/create/', CreatePermissionView.as_view(), name='create_permission'),
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
]

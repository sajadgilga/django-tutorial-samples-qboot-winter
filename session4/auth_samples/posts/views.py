import json

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DetailView, ListView

from posts.models import Post


class ViewCounterMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.model._default_manager.get(pk=kwargs['pk'])
        post.view_count += 1
        post.save()
        self.view_count = post.view_count
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(view_count=self.view_count)


class PostDetailView(ViewCounterMixin, DetailView):
    model = Post
    template_name = 'post.html'


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostEditView(UpdateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'text']
    pk_url_kwarg = 'post_pk'
    permission_required = ['change_post']

    # def post(self, request, *args, **kwargs):
    #     # First way to check user permission
    #     if request.user.user_permissions.filter(codename="change_post").exists():
    #         return super().post(request, *args, **kwargs)
    #
    #     # Second way to check user permission
    #     if request.user.has_perm("change_post"):
    #         return super().post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class PublishPostView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['posts.can_publish']

    def has_permission(self):
        return self.request.user.has_perms(self.get_permission_required())

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponseNotFound()
        post.published = True
        post.save()
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class CreatePermissionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def handle_no_permission(self):
        return HttpResponse("Use must be authenticated to call this api", status=401)

    def has_permission(self):
        return self.user.groups.filter(name="PostAdmin").exists()

    def post(self, request):
        body = json.loads(request.body)
        codename, name, group_name = body["permission_name"], body["description"], body["group_name"]
        content_type = ContentType.objects.get(model="post", app_label="posts")
        perm = Permission.objects.create(codename=codename, name=name, content_type=content_type)
        request.user.user_permissions.add(perm)
        group = Group.objects.get(name=group_name)
        group.permissions.add(perm)
        return HttpResponse(f"permission {perm.name} created successfully and added to group {group.name}")


@method_decorator(csrf_exempt, name="dispatch")
class CreateGroupView(View):
    def post(self, request):
        body = json.loads(request.body)
        name = body["name"]
        group = Group.objects.create(name=name)
        return HttpResponse(f"group {group.name} created successfully")

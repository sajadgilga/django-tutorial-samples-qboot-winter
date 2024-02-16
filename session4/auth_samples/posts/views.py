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


class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'text']
    pk_url_kwarg = 'post_pk'

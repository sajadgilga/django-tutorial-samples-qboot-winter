from datetime import datetime, timedelta

from django.db.models import Q, F
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render

from posts.forms import post_formset, book_formset
from posts.models import Post, Comment, PostTemplate, Book


# Max 3 queries to db, Min 1 query to db
def retrieve_posts(request):
    filter_exp = Q()

    if 'title' in request.GET.keys():
        filter_exp &= Q(title__in=request.GET.getlist('title'))

    if 'content' in request.GET.keys():
        filter_exp |= Q(content=request.GET.get('content'))

    posts = Post.objects.filter(~filter_exp)
    # is equal to: posts = Post.objects.exclude(filter_exp)
    message = f'post count: {posts.count()}'
    return HttpResponse(message)


def retrieve_posts_exclude_sample(request):
    posts = Post.objects.all()

    if 'title' in request.GET.keys():
        posts = posts.exclude(title=request.GET.get('title'))

    posts = posts.order_by('-title', 'content')
    posts = posts.filter(created_date__range=(datetime.now() - timedelta(hours=1), datetime.now()))

    # message = f'post count: {posts.count()}'
    return HttpResponse(posts.only('title').values_list('title', flat=True))


def retrieve_posts_with_equal_content_title(request):
    # python way to find posts with equal content & title
    # posts = []
    # for post in Post.objects.all():
    #     if post.title == post.content:
    #         posts.append(post)

    # db (orm) way to find posts with equal content & title
    posts = Post.objects.filter(title=F('content')).annotate(view_like_avg=F('like_count') + F('view_count'))

    return HttpResponse(posts.values_list('title', 'content', 'view_like_avg'))


def get_comments(request):
    now = datetime.now()
    comments = Comment.objects.filter(post__title__contains='post', created_date__range=(now - timedelta(hours=1), now))

    # first way to get posts which have a comment with text='something'
    Post.objects.filter(my_comments__text__contains='something')

    # second way to get posts which have a comment with text='something'
    comments = Comment.objects.filter(text__contains='something')
    Post.objects.filter(my_comments__in=comments)
    return HttpResponse(comments.values_list('text', flat=True))


def add_templates(request):
    now = datetime.now()
    PostTemplate.objects.create(title_template='some other template', content_template='')
    new_template = PostTemplate.objects.all()
    post = Post.not_archived.first()
    post.templates.set(new_template)
    return HttpResponse('done')


def view_template(request):
    if 'post_id' in request.GET.keys():
        post = Post.objects.get(pk=request.GET.get('post_id'))
    else:
        posts = Post.objects.exclude(title=F('content'))
        return render(request, 'posts.html',
                      context={'title': 'My post list', 'posts': posts})

    if request.method == 'POST':
        form = post_formset(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'post_detail.html', context={'form': form, 'post': post})
        print('not valid', form.error_messages)
        return render(request, 'post_detail.html', context={'form': form, 'post': post})

    form = post_formset(queryset=Post.objects.filter(title__contains='some'))
    return render(request, 'post_detail.html', context={
        'post': post,
        'form': form,
    })


def library_view(request):
    library = request.GET.get('library', 1)
    if request.method == 'GET':
        formset = book_formset(queryset=Book.objects.filter(library_id=library))
        return render(request, 'book.html', context={
            'formset': book_formset
        })
    elif request.method == 'POST':
        formset = book_formset(request.POST, queryset=Book.objects.filter(library_id=library))
        if formset.is_valid():
            formset.save(commit=True)
        return render(request, 'book.html', context={
            'formset': book_formset
        })

    return HttpResponse('method not allowed', status=405)

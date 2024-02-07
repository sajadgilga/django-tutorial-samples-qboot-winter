import csv
import json
from time import sleep

from django.http import JsonResponse, FileResponse, StreamingHttpResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create, Retrieve, Update, Delete (CRUD)
from posts.models import Post


def retrieve_posts(request):
    posts = list(Post.objects.all()[:10].values_list('title', flat=True))
    return render(request, 'post_content.html', {'posts': posts})

    # second way to render template
    # template = loader.get_template('post_content.html')
    # rendered_template = template.render({'post': post}, request)
    # return HttpResponse(rendered_template)


class PostEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Post):
            return {
                'title': o.title,
                'content': o.content
            }
        return super().default(o)


def retrieve_post_info(request, pk, name=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound(f'Post with id {pk} not found')
    return JsonResponse(post, encoder=PostEncoder, safe=False)


def retrieve_post_file(request, pk, name=None):
    print(f'Retrieve info called for post-{pk}: {name}')
    file = open('./static/Screenshotmorning.png', 'rb')
    response = FileResponse(file, content_type='image/png')
    # For auto downloading
    response['Content-Disposition'] = f'attachment; filename="Screenshot-{pk}.png"'
    return response


def generate_post_csv():
    for i in range(100):
        if i % 10 == 0:
            sleep(.5)
        yield [i, f'data_{i}', f'another column {i}']


def retrieve_post_text(request):
    writer = csv.writer(CSVWriter())
    response = StreamingHttpResponse((writer.writerow(row) for row in generate_post_csv()), content_type='text/csv')
    return response


class CSVWriter:
    def write(self, value):
        return value


@csrf_exempt
# @login_required
@require_http_methods(['POST'])
def create_post(request):
    # Form data
    # post_title = request.POST.get('title')
    # post_content = request.POST.get('content')
    # print(f'Post {post_title} with content {post_content} created')

    # json body
    body = json.loads(request.body)
    if 'title' not in body or 'content' not in body:
        return JsonResponse({'message': 'title & body must be sent to create new post'}, status=400)
    try:
        print(f'Post {body["title"]} created with json mode')
        # First type of creating model:
        # Post.objects.create(title=body['title'], content=body['content'], author_id=2)
        # Second type of creating model:
        p = Post(title=body['title'], author_id=2)
        p.content = body['content']
        p.save()
    except KeyError as e:
        print('body has no title')
    return HttpResponse('post created', status=201)

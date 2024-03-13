# Create your views here.
import asyncio
import json
import os
from datetime import datetime, timedelta
from io import BytesIO
from time import sleep

from PIL import Image
from asgiref.sync import sync_to_async
from celery import shared_task, chain
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.generics import CreateAPIView

from authentication.models import OTPCode, Book, ImageUpload
from authentication.serializers import RequestOTPSerializer, ImageUploadSerializer


class RequestOTPView(CreateAPIView):
    serializer_class = RequestOTPSerializer

    def perform_create(self, serializer):
        pass


async def operation():
    await asyncio.sleep(1)
    print('some operation done')


@shared_task
def compute_power(x, p):
    return x ** p


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retires': 3, 'countdown': 4})
def sample_task(self, val):
    try:
        sleep(3)
        raise Exception('failed')
        print('my task has run:', val)
        return len(val)
    except Exception as exc:
        self.retry(args=(val,), exc=exc, countdown=3, max_retries=3, queue="important")


@shared_task
def heavy_computation(val):
    cache_key = f'heavy_computation:{len(val)}'
    cache_result = cache.get(cache_key)
    if cache_result:
        print('my heavy task has been read from cache:', cache_result)
        return cache_result
    c = 0
    for i in range(100):
        for j in range(100):
            c += i / (j + 1)
    print('my heavy task has run:', c)
    cache.set(cache_key, c)
    return c


def sample_view(request):
    param = request.GET.get("param", "default")
    cache_key = f'{request.method}-{request.path}-{param}'
    cache_result = cache.get(cache_key)
    if cache_result:
        return HttpResponse(cache_result)
    sleep(2)
    print('sample view run!')
    s1 = compute_power.s(3, 2)
    chain(s1, compute_power.s(2))()
    sample_task.apply_async(("hello",), eta=datetime.now() + timedelta(seconds=2), task_id="my_task_id",
                            queue="important")

    heavy_computation.apply_async((param,), task_id="my_task_id",
                                  queue="comp")
    message = 'hello'
    cache.set(cache_key, message, 20)
    return HttpResponse(message)


def some_sync_operation(val):
    sleep(.5)
    return val * 2


class SampleView(View):
    async def get(self, request):
        r = await sync_to_async(some_sync_operation)(20)
        o = await OTPCode.objects.afirst()
        return HttpResponse(f'class based view {r}')


class CreateBookView(View):
    async def post(self, request):
        books_data = json.loads(request.body)
        books = []
        for book_data in books_data:
            books.append(Book.objects.acreate(name=book_data['name']))

        await asyncio.gather(*books)

        return JsonResponse({'message': 'books created'})


@shared_task
def generate_thumbail(img_id):
    img = ImageUpload.objects.get(id=img_id)

    original = Image.open(img.original_image)
    original.thumbnail((200, 200))
    thumb_name, thumb_extension = os.path.splitext(img.original_image.name.split('/')[1])
    thumb_name += '_thumb' + thumb_extension

    temp_bytes = BytesIO()
    original.save(temp_bytes, format='JPEG')
    temp_bytes.seek(0)

    temp_file = ContentFile(temp_bytes.read())
    temp_bytes.close()
    img.thumbnail_image.save(thumb_name, temp_file, save=False)
    img.save()


class ImageUploadView(CreateAPIView):
    serializer_class = ImageUploadSerializer
    queryset = ImageUpload.objects.all()

    def perform_create(self, serializer):
        img = serializer.save()
        generate_thumbail.delay(img.id)

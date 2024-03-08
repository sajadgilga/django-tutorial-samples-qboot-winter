# Create your views here.
import asyncio
import json
from datetime import datetime, timedelta
from time import sleep

from asgiref.sync import sync_to_async
from celery import shared_task, chain
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.generics import CreateAPIView

from authentication.models import OTPCode, Book
from authentication.serializers import RequestOTPSerializer


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
    c = 0
    for i in range(100000):
        for j in range(1000000):
            c += i / (j + 1)
    print('my heavy task has run:', val)


def sample_view(request):
    s1 = compute_power.s(3, 2)
    chain(s1, compute_power.s(2))()
    sample_task.apply_async(("hello",), eta=datetime.now() + timedelta(seconds=2), task_id="my_task_id",
                            queue="important")

    heavy_computation.apply_async(("hello",), eta=datetime.now() + timedelta(seconds=20), task_id="my_task_id",
                                  queue="computation")
    return HttpResponse('hello')


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

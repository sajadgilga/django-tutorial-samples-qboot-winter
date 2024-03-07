# Create your views here.
import asyncio
import json
from time import sleep

from asgiref.sync import sync_to_async
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


async def sample_view(request):
    await operation()
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

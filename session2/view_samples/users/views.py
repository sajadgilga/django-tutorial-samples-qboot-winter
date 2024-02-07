import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

User = get_user_model()


@csrf_exempt
@cache_page(timeout=10)
@require_http_methods(['GET', 'PATCH', 'DELETE'])
def get_profile(request, user_id, username=None):
    if request.method == 'GET':
        q_param = request.GET.getlist('x')
        print(f'User profile called for user-{user_id} with username: {username} -- queries: {q_param}')
        return HttpResponse(f'User {user_id} with username {username} returned! -- queries: {q_param}')
    elif request.method == 'PATCH':
        body = json.loads(request.body)
        first_name, last_name = body['first_name'], body['last_name']
        print('first name and last name is:', first_name, last_name)
        user = User.objects.get(pk=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return HttpResponse(f'Profile {user_id} Updated', status=201)
    elif request.method == 'DELETE':
        return HttpResponse('Profile deleted', status=201)

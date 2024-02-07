from django.urls import re_path

from users.views import get_profile

urlpatterns = [
    re_path(r'profile/(?P<user_id>\d{1,4})/$', get_profile),
    re_path(r'profile/(?:user-(?P<user_id>\d{1,4}))/$', get_profile),
    # path capturing both inside & outside parameter
    # re_path(r'profile/(?P<username>user-(?P<user_id>\d{1,4}))/$', get_profile),
    re_path(r'profile/(?P<user_id>\d{1,4})/(?:(?P<username>\w{6})/)?$', get_profile),
]

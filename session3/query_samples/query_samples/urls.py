"""
URL configuration for query_samples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import retrieve_posts, retrieve_posts_exclude_sample, retrieve_posts_with_equal_content_title, \
    add_templates, view_template, library_view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('posts/', retrieve_posts),
                  path('posts/exclude/', retrieve_posts_exclude_sample),
                  path('posts/same-title/', retrieve_posts_with_equal_content_title),
                  path('posts/add-template/', add_templates),
                  path('posts/template/', view_template),
                  path('books/', library_view),
                  path('football/', include('football.urls'))
              ] + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

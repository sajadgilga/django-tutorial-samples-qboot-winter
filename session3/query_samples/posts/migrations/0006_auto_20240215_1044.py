# Generated by Django 4.2.9 on 2024-02-15 10:44

from django.db import migrations


def fill_engagement_count(app, schema_editor):
    Post = app.get_model('posts', 'Post')


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0005_add_library_models'),
    ]

    operations = [
    ]

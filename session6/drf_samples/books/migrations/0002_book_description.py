# Generated by Django 4.2.9 on 2024-02-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

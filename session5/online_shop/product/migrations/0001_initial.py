# Generated by Django 4.2.9 on 2024-02-23 08:55

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url='/static/products', location='static/products'), upload_to='')),
                ('default_price', models.PositiveIntegerField()),
                ('fellow_price', models.PositiveIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=64)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

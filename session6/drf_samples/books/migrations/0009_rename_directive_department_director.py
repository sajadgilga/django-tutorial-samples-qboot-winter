# Generated by Django 4.2.9 on 2024-03-01 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='directive',
            new_name='director',
        ),
    ]
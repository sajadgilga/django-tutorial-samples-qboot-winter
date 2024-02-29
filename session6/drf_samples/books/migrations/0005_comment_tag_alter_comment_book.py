# Generated by Django 4.2.9 on 2024-02-29 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tag',
            field=models.CharField(default='default', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='books.book'),
        ),
    ]

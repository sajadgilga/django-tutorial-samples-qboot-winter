# Generated by Django 4.2.9 on 2024-02-08 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_posttemplate_comment_post_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='templates',
            field=models.ManyToManyField(related_name='posts', to='posts.posttemplate'),
        ),
    ]

# Generated by Django 4.2.6 on 2024-01-27 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworks', '0020_noticetype_notice_noticetype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='follow',
        ),
        migrations.RemoveField(
            model_name='notice',
            name='post',
        ),
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

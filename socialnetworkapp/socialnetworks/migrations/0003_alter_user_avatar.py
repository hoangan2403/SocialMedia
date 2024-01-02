# Generated by Django 4.2.6 on 2023-12-30 14:35

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworks', '0002_reporttype_content_alter_auction_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='avatar'),
        ),
    ]

# Generated by Django 4.2.6 on 2024-01-12 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworks', '0011_alter_like_like_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='comments', to='socialnetworks.post'),
        ),
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_query_name='images', to='socialnetworks.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='like_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='socialnetworks.liketype'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='like', to='socialnetworks.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_hashtag',
            field=models.ManyToManyField(null=True, related_query_name='hashtag', to='socialnetworks.hashtag'),
        ),
    ]
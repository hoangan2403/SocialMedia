# Generated by Django 4.2.6 on 2024-01-11 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworks', '0010_alter_like_like_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='socialnetworks.liketype'),
        ),
    ]
# Generated by Django 4.2.6 on 2024-01-14 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworks', '0014_alter_auction_product_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_query_name='auction', to='socialnetworks.product'),
        ),
    ]

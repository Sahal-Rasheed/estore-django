# Generated by Django 4.1.5 on 2023-02-06 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_in_wishlist'),
        ('cart', '0004_remove_wishlist_product_wishlist_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]

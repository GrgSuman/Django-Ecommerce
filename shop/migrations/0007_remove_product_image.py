# Generated by Django 3.1.5 on 2021-01-14 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_img_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]

# Generated by Django 5.1.1 on 2024-12-05 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_product_picture_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]

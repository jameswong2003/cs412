# Generated by Django 5.1.1 on 2024-11-21 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_delete_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_transaction', models.DateField()),
                ('boughtbyBusiness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bought_by', to='project.business')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='project.product')),
                ('soldByBusiness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_by', to='project.business')),
            ],
        ),
    ]

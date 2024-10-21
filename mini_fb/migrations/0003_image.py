# Generated by Django 5.1.1 on 2024-10-20 22:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_statusmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='images/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mini_fb.statusmessage')),
            ],
        ),
    ]

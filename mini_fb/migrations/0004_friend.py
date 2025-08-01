# Generated by Django 5.2.1 on 2025-06-05 15:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image_statusimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile1', to='mini_fb.profile')),
                ('profile2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile2', to='mini_fb.profile')),
            ],
        ),
    ]

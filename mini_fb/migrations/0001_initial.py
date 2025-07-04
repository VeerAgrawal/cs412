# Generated by Django 5.2.1 on 2025-05-27 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.TextField(blank=True)),
                ('lastName', models.TextField(blank=True)),
                ('city', models.TextField(blank=True)),
                ('email', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
            ],
        ),
    ]

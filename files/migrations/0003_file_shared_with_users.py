# Generated by Django 4.2.3 on 2023-07-25 04:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0002_file_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='shared_with_users',
            field=models.ManyToManyField(blank=True, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
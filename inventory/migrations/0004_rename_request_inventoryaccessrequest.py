# Generated by Django 5.1.1 on 2024-10-13 10:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_request_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='InventoryAccessRequest',
        ),
    ]

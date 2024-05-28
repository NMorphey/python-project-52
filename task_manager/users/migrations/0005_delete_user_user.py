# FIX for broken migrations

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_customuser_user'),
    ]

    operations = []

# Generated by Django 5.0.6 on 2024-05-21 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_task_author_alter_task_description_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]

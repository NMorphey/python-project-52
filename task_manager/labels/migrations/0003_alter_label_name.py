# Generated by Django 5.0.6 on 2024-05-21 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_remove_label_tasks_delete_tasklabelrelationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
    ]

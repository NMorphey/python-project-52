# Generated by Django 5.0.6 on 2024-05-18 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_remove_label_tasks_delete_tasklabelrelationship'),
        ('tasks', '0004_tasklabelrelationship_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, through='tasks.TaskLabelRelationship', to='labels.label'),
        ),
    ]

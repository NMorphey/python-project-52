from django.db import models
from task_manager.tasks.models import Task


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(Task, through='TaskLabelRelationship')

    def __str__(self) -> str:
        return self.name


class TaskLabelRelationship(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

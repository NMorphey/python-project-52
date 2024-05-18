from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='created_tasks'
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True,
        null=True, related_name='executing_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label, blank=True, through='TaskLabelRelationship'
    )

    def __str__(self) -> str:
        return self.name


class TaskLabelRelationship(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

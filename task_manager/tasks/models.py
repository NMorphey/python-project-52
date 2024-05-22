from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('Name')
    )
    description = models.TextField(
        blank=True, null=True, verbose_name=_('Description')
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='created_tasks', verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True,
        related_name='executing_tasks', verbose_name=_('Executor')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label, blank=True, through='TaskLabelRelationship',
        verbose_name=_('Labels')
    )

    def __str__(self) -> str:
        return self.name


class TaskLabelRelationship(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

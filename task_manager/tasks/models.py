from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='executing_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

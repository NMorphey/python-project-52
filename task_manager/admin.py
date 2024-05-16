from django.contrib import admin
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

admin.site.register(User)
admin.site.register(Status)
admin.site.register(Task)

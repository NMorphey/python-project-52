from django.contrib import admin
from task_manager.users.models import User
from task_manager.statuses.models import Status

admin.site.register(User)
admin.site.register(Status)

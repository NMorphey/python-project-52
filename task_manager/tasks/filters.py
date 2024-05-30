import django_filters
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label=_('Status')
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label=_('Executor')
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), field_name='labels', label=_('Label')
    )
    self_tasks = django_filters.BooleanFilter(
        widget=CheckboxInput,
        method='filter_self_tasks',
        label=_('My own tasks only')
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

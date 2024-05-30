from django.views.generic import DetailView
from task_manager.tasks.models import Task
from task_manager.utils import LoginRequiredMixin
from task_manager.tasks.filters import TaskFilter
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class TasksIndexView(LoginRequiredMixin, FilterView):
    template_name = 'tasks/index.html'
    model = Task
    fields = ['id', 'name', 'status', 'author', 'executor', 'created_at']
    filterset_class = TaskFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = TaskFilter(
            self.request.GET, queryset=queryset, request=self.request
        )
        return filter.qs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/details.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'common/create.html'
    success_message = _('Task created successfully')
    success_url = reverse_lazy('task_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Create task')
        return context

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'common/update.html'
    success_message = _('The task was updated')
    success_url = reverse_lazy('task_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Edit task')
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'common/delete.html'
    success_message = _('The task was deleted')
    success_url = reverse_lazy('task_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Delete task')
        return context

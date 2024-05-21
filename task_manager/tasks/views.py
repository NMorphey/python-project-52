from django.shortcuts import redirect
from django.views.generic import DetailView
from task_manager.utils import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.utils import LoginRequiredMixin, error_flash
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.tasks.filters import TaskFilter
from django.utils.translation import gettext_lazy as _


class TasksIndexView(ListView):
    model = Task
    fields = ['id', 'name', 'status', 'author', 'executor', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = TaskFilter(
            self.request.GET, queryset=queryset, request=self.request
        )
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(
            self.request.GET,
            queryset=self.get_queryset(),
            request=self.request
        )
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/details.html'
    context_object_name = 'task'


class TaskDeleteView(DeleteView):
    model = Task

    def dispatch(self, request, *args, **kwargs):
        if Task.objects.get(id=kwargs['pk']).author.id != request.user.id:
            error_flash(request, 'A task can only be deleted by its author')
            return redirect('tasks_index')
        return super().dispatch(request, *args, **kwargs)


class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']

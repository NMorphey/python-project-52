from django.forms import BaseForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.utils import LoginRequiredMixin, error_flash
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.tasks.filters import TaskFilter


class TasksIndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = TaskFilter(self.request.GET, queryset=queryset, request=self.request)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(self.request.GET, queryset=self.get_queryset(), request=self.request)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/details.html'
    context_object_name = 'task'


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'The task was deleted'

    def dispatch(self, request, *args, **kwargs):
        if Task.objects.get(id=kwargs['pk']).author.id != request.user.id:
            error_flash(request, 'A task can only be deleted by its author')
            return redirect('tasks_index')
        return super().dispatch(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = 'Task created successfully'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = 'The task was updated'

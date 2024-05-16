from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from task_manager.statuses.models import Status
from task_manager.utils import LoginRequiredMixin


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')

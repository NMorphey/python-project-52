from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.statuses.models import Status


class StatusesIndexView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')


class StatusCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'statuses/create.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'statuses/update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')

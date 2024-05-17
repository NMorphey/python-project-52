from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.statuses.models import Status
from task_manager.utils import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from task_manager.utils import error_flash
from django.db.models.deletion import ProtectedError


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('The status was deleted')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned status cannot be deleted')
            return redirect('statuses_index')


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status created successfully')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_index')
    success_message = _('The status was updated')

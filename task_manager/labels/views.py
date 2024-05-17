from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from task_manager.utils import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from task_manager.utils import error_flash
from django.db.models.deletion import ProtectedError


class LabelsIndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('The label was deleted')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned label cannot be deleted')
            return redirect('labels_view')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    fields = ['name']
    success_url = reverse_lazy('labels_index')
    success_message = _('Label created successfully')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    fields = ['name']
    success_url = reverse_lazy('labels_index')
    success_message = _('The label was updated')

from django.shortcuts import redirect
from task_manager.labels.models import Label
from django.contrib.messages import error
from django.db.models.deletion import ProtectedError
from task_manager.utils import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class LabelsIndexView(LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    model = Label
    fields = ['id', 'name', 'created_at']


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'common/create.html'
    success_message = _('Label created successfully')
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Create label')
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'common/update.html'
    success_message = _('The label was updated')
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Edit label')
        return context


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'common/delete.html'
    success_message = _('The label was deleted')
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Delete label')
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error(request, _('Assigned label cannot be deleted'))
            return redirect('label_index')

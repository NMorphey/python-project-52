from task_manager.labels.models import Label
from task_manager.utils import LoginRequiredMixin, HandleProtectedError
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


class LabelDeleteView(LoginRequiredMixin, HandleProtectedError,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'common/delete.html'
    success_message = _('The label was deleted')
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Delete label')
        return context

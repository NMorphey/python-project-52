from django.shortcuts import redirect
from task_manager.statuses.models import Status
from django.contrib.messages import error
from django.db.models.deletion import ProtectedError
from task_manager.utils import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class StatusesIndexView(LoginRequiredMixin, ListView):
    template_name = 'statuses/index.html'
    model = Status
    fields = ['id', 'name', 'created_at']


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'common/create.html'
    success_message = _('Status created successfully')
    success_url = reverse_lazy('status_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Create status')
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'common/update.html'
    success_message = _('The status was updated')
    success_url = reverse_lazy('status_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Edit status')
        return context


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'common/delete.html'
    success_message = _('The status was deleted')
    success_url = reverse_lazy('status_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = _('Delete status')
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error(request, _('Assigned status cannot be deleted'))
            return redirect('status_index')

from django.shortcuts import redirect
from task_manager.utils import ListView, CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Status
from task_manager.utils import error_flash
from django.db.models.deletion import ProtectedError


class StatusesIndexView(ListView):
    model = Status
    fields = ['id', 'name', 'created_at']


class StatusDeleteView(DeleteView):
    model = Status

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned status cannot be deleted')
            return redirect('statuses_index')


class StatusCreateView(CreateView):
    model = Status
    fields = ['name']


class StatusUpdateView(UpdateView):
    model = Status
    fields = ['name']

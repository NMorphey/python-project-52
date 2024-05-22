from django.shortcuts import redirect
from task_manager.utils import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.utils import error_flash
from django.db.models.deletion import ProtectedError


class LabelsIndexView(ListView):
    model = Label
    fields = ['id', 'name', 'created_at']


class LabelDeleteView(DeleteView):
    model = Label

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned label cannot be deleted')
            return redirect('label_index')


class LabelCreateView(CreateView):
    model = Label
    fields = ['name']


class LabelUpdateView(UpdateView):
    model = Label
    fields = ['name']

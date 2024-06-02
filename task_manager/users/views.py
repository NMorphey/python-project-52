from django.shortcuts import redirect
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.utils import LoginRequiredMixin
from django.contrib.messages import error
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from django.contrib.auth.mixins import UserPassesTestMixin


class UsersIndexView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'


class RegistrationView(SuccessMessageMixin, CreateView):

    model = User
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user created successfully')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin,
                     UserPassesTestMixin, UpdateView):

    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_index')
    success_message = _('User updated successfully')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        error(self.request, _('You are not authorized to modify other users.'))
        return redirect(reverse_lazy('user_index'))


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin,
                     UserPassesTestMixin, DeleteView):

    model = User
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_index')
    success_message = _('User deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error(request, _('Assigned user cannot be deleted'))
            return redirect('user_index')

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        error(self.request, _('You are not authorized to modify other users.'))
        return redirect(reverse_lazy('user_index'))

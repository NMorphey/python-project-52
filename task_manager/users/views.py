from django.shortcuts import redirect
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.utils import error_flash, LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from task_manager.users.utils import check_access_to_modify


User = get_user_model()


class UsersIndexView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'


class RegistrationView(SuccessMessageMixin, CreateView):

    model = User
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users_index')
    success_message = _('The user created successfully')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users_index')
    success_message = _('User updated successfully')

    @check_access_to_modify
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users_index')
    success_message = _('User deleted successfully')

    @check_access_to_modify
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned user cannot be deleted')
            return redirect('users_index')

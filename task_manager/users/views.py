from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from task_manager.users.forms import UserForm
from task_manager.utils import success_flash, error_flash, LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersIndexView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'users/create.html',
            {'form': UserForm()}
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            success_flash(request, 'The user created successfully')
            return redirect('login')
        return render(
            request,
            'users/create.html',
            {'form': form}
        )


class UpdateUserView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if request.user.id != id:
            error_flash(
                request, 'You are not authorized to modify other users.'
            )
            return redirect('users_index')
        user = get_object_or_404(User, id=id)
        form = UserForm(instance=user)
        return render(request, 'users/update.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        if request.user.id != id:
            error_flash(
                request, 'You are not authorized to modify other users.'
            )
            return redirect('users_index')

        form = UserForm(request.POST)
        if str(_('A user with that username already exists.')) \
                in str(form.errors):
            form.errors.pop('username')
            form.cleaned_data['username'] = form.data['username']
        if form.is_valid():
            user = User.objects.get(id=id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            success_flash(request, 'User updated successfully')
            return redirect('users_index')
        return render(
            request,
            'users/update.html',
            {'form': form, 'id': id}
        )


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users_index')
    success_message = _('User deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.id:
            error_flash(
                request, 'You are not authorized to modify other users.'
            )
            return redirect('users_index')
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            error_flash(request, 'Assigned user cannot be deleted')
            return redirect('users_index')

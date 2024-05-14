from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UsersIndexView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'users/index.html',
            {
                'users': User.objects.all().values(
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                    'date_joined'
                )
            }
        )


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'users/registration.html',
            {'form': UserForm()}
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(
            request,
            'users/registration.html',
            {'form': form}
        )


class UpdateUserView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        id = kwargs['id']
        if request.user.id != id:
            return redirect('users_index')
        user = get_object_or_404(User, id=id)
        form = UserForm(instance=user)
        return render(request, 'users/update_user.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        id = kwargs['id']
        if request.user.id != id:
            return redirect('users_index')

        form = UserForm(request.POST)
        username_exists_is_the_only_error = (
            len(form.errors) == 1
            and 'A user with that username already exists.' in str(form.errors)
        )
        if username_exists_is_the_only_error:
            form.cleaned_data['username'] = form.data['username']
        if form.is_valid() or username_exists_is_the_only_error:
            user = User.objects.get(id=id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('users_index')
        return render(
            request,
            'users/update_user.html',
            {'form': form, 'id': id}
        )


class DeleteUserView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        id = kwargs['id']
        if request.user.id != id:
            return redirect('users_index')
        user = get_object_or_404(User, id=id)
        form = UserForm(instance=user)
        return render(request, 'users/delete_user.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        id = kwargs['id']
        if request.user.id != id:
            return redirect('users_index')
        User.objects.get(id=id).delete()
        return redirect('users_index')

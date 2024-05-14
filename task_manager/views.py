from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from task_manager.users.forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LogInView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'form': AuthenticationForm()})

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request=request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('main_page')
        form = AuthenticationForm(data=request.POST)
        return render(request, 'login.html', {'form': form})


class LogOutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('main_page')

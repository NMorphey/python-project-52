from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from task_manager.utils import info_flash, success_flash


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
            success_flash(request, 'Logged in successfully')
            return redirect('main_page')
        form = AuthenticationForm(data=request.POST)
        return render(request, 'login.html', {'form': form})


class LogOutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        info_flash(request, 'Logged out')
        return redirect('main_page')

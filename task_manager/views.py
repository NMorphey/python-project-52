from django.views import View
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.utils import success_flash
from django.utils.translation import gettext_lazy as _


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class CustomLoginView(SuccessMessageMixin, LoginView):

    success_message = _('Logged in successfully')


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        success_flash(request, 'Logged out')
        return response

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.test import TestCase, Client


# Flash-messages
def success_flash(request, message):
    messages.success(request, _(message))


def error_flash(request, message):
    messages.error(request, _(message))


def info_flash(request, message):
    messages.info(request, _(message))


# Mixin
class LoginRequiredMixin(LRM):

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('This can be done only by an authenticated user!')
        )
        return redirect(reverse_lazy('login'))


# Tests Mixins
class SetUpClient(TestCase):

    def setUp(self):
        self.client = Client()


class SetUpUsers(SetUpClient):

    def setUp(self):
        super().setUp()

        self.user_1_data = {
            'first_name': 'User',
            'last_name': 'Testov',
            'username': 'test_user',
            'password1': 'qwerty',
            'password2': 'qwerty'
        }
        self.user_1_login_data = {
            'username': self.user_1_data['username'],
            'password': self.user_1_data['password1']
        }
        self.client.post(reverse_lazy('registration'), self.user_1_data)

        self.user_2_data = {
            'first_name': 'User',
            'last_name': 'Another',
            'username': 'another_user',
            'password1': 'qwerty',
            'password2': 'qwerty'
        }
        self.user_2_login_data = {
            'username': self.user_2_data['username'],
            'password': self.user_2_data['password1']
        }
        self.client.post(reverse_lazy('registration'), self.user_2_data)


class SetUpSignedInClient(SetUpUsers):

    def setUp(self):
        super().setUp()
        self.client.post(reverse_lazy('login'), self.user_1_login_data)


class SetUpStatus(SetUpSignedInClient):

    def setUp(self):
        super().setUp()
        self.status_name = 'test_status'
        self.client.post(reverse_lazy('create_status'), {'name': self.status_name})

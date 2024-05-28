from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.test import TestCase, Client
from django.views.generic import (
    ListView as _ListView,
    CreateView as _CreateView,
    UpdateView as _UpdateView,
    DeleteView as _DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import get_messages


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
        self.client.post(reverse_lazy('status_create'),
                         {'name': self.status_name})


class SetUpLabel(SetUpSignedInClient):

    def setUp(self):
        super().setUp()
        self.label_name = 'test_label'
        self.client.post(reverse_lazy('label_create'),
                         {'name': self.label_name})


class CheckFlashMixin:

    def check_flash(self, response, message):
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[-1]), _(message))


# Customized generic view

class ListView(LoginRequiredMixin, _ListView):
    template_name = 'common/index.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = self.__class__.model.__name__.lower()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Trying to render details link. There is no view if error occures
            # Can be replaced with "if self.__class__.model == Task: ..."
            # But this is more generic way to check
            reverse_lazy(f'{self.model_name}_details', kwargs={'pk': 1})[:]
            context['has_details_view'] = True
        except Exception:
            context['has_details_view'] = False
        context['model_name'] = self.model_name
        model_name_plural = _(
            self.model_name.capitalize()
            + 'e' * (self.model_name[-1] == 's')
            + 's')
        context['model_name_plural'] = model_name_plural
        context['fields'] = self.__class__.fields
        context['field_headers'] = list(map(
            # replace() is for created_at
            lambda field: _(field.replace('_', ' ').capitalize())
            if field.lower() != 'id'
            else 'ID',
            self.__class__.fields
        ))
        context['create_button_label'] = _(f'Create {self.model_name}')
        return context

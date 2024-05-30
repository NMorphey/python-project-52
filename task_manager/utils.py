from django.contrib.messages import error
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.test import TestCase
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


# Mixin
class LoginRequiredMixin(LRM):

    def handle_no_permission(self):
        error(
            self.request,
            _('This can be done only by an authenticated user!')
        )
        return redirect(reverse_lazy('login'))


# Tests Mixins

class SetUpTestCase(TestCase):

    fixtures = [
        'task_manager/fixtures/users_fixture.json',
        'task_manager/fixtures/statuses_fixture.json',
        'task_manager/fixtures/labels_fixture.json',
        'task_manager/fixtures/tasks_fixture.json']

    def setUp(self):
        super().setUp()

        User = get_user_model()

        self.user_1 = User.objects.get(username='test_user')
        self.user_2 = User.objects.get(username='another_user')
        self.user_3 = User.objects.get(username='unused_user')
        self.user_1_login_data = {
            'username': self.user_1.username, 'password': 'qwerty'}
        self.user_2_login_data = {
            'username': self.user_2.username, 'password': 'qwerty'}
        self.user_3_login_data = {
            'username': self.user_3.username, 'password': 'qwerty'}

        self.status_1 = Status.objects.get(name='status1')
        self.status_2 = Status.objects.get(name='status2')
        self.unused_status = Status.objects.get(name='unused_status')

        self.label_1 = Label.objects.get(name='label1')
        self.label_2 = Label.objects.get(name='label2')
        self.label_3 = Label.objects.get(name='label3')
        self.unused_label = Label.objects.get(name='unused_label')

        self.task_1 = Task.objects.get(name='task1')
        self.task_2 = Task.objects.get(name='task2')
        self.task_3 = Task.objects.get(name='task3')


class SetUpSignedInClient(SetUpTestCase):

    def setUp(self):
        super().setUp()
        self.client.post(reverse_lazy('login'), self.user_1_login_data)


class CheckFlashMixin:

    def check_flash(self, response, message):
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[-1]), _(message))

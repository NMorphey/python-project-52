from django.urls import reverse_lazy
from task_manager.utils import (
    SetUpTestCase, SetUpSignedInClient
)
from django.utils.translation import gettext_lazy as _


class UnavailableForGuestsTestCase(SetUpTestCase):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('task_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('task_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('task_index'), follow=True)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(
            response,
            _('This can be done only by an authenticated user!'))


class CRUDTestCase(SetUpSignedInClient):

    def test_create(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, 'created_task')

        response = self.client.post(
            reverse_lazy('task_create'),
            {'name': 'created_task', 'status': 1},
            follow=True)
        self.assertRedirects(response, reverse_lazy('task_index'))
        self.assertContains(response, _('Task created successfully'))

        response = self.client.get(reverse_lazy('task_index'))
        self.assertContains(response, 'created_task')

    def test_setup(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertContains(response, self.task_1.name)

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': self.task_1.pk}),
            follow=True)
        self.assertRedirects(response, reverse_lazy('task_index'))
        self.assertContains(response, _('The task was deleted'))

        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, self.task_1.name)

    def test_update(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, 'renamed_task')

        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': self.task_1.pk}),
            {'name': 'renamed_task', 'status': 1}, follow=True)
        self.assertRedirects(response, reverse_lazy('task_index'))
        self.assertContains(response, _('The task was updated'))

        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, self.task_1.name)
        self.assertContains(response, 'renamed_task')


class QueryTestCase(SetUpTestCase):

    def setUp(self):
        super().setUp()
        self.client.post(reverse_lazy('login'), self.user_2_login_data)

    def test_status_search(self):
        response = self.client.get(reverse_lazy('task_index'), {'status': 1})
        self.assertContains(response, self.task_1.name)
        self.assertNotContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)

    def test_executor_search(self):
        response = self.client.get(reverse_lazy('task_index'),
                                   {'executor': 1})
        self.assertNotContains(response, self.task_1.name)
        self.assertContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)

    def test_self_search(self):
        response = self.client.get(reverse_lazy('task_index'),
                                   {'self_tasks': 'on'})
        self.assertNotContains(response, self.task_1.name)
        self.assertNotContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)

    def test_lables_search(self):
        response = self.client.get(reverse_lazy('task_index'), {'label': 1})
        self.assertContains(response, self.task_1.name)
        self.assertContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)

        response = self.client.get(reverse_lazy('task_index'), {'label': 2})
        self.assertContains(response, self.task_1.name)
        self.assertNotContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)

        response = self.client.get(reverse_lazy('task_index'), {'label': 3})
        self.assertNotContains(response, self.task_1.name)
        self.assertNotContains(response, self.task_2.name)
        self.assertNotContains(response, self.task_3.name)

    def test_multiple_searches(self):
        response = self.client.get(
            reverse_lazy('task_index'),
            {'label': 1, 'self_tasks': 'on', 'executor': 1, 'status': 1}
        )
        self.assertNotContains(response, self.task_1.name)
        self.assertNotContains(response, self.task_2.name)
        self.assertContains(response, self.task_3.name)


class ProtectionsTestCase(SetUpTestCase):

    def setUp(self):
        super().setUp()
        self.client.post(reverse_lazy('login'), self.user_2_login_data)

    def test_protections(self):
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirects(response, reverse_lazy('label_index'))
        self.assertContains(response, _('Assigned label cannot be deleted'))

        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.assertContains(response, _('Assigned status cannot be deleted'))

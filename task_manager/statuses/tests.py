from django.urls import reverse_lazy
from task_manager.utils import SetUpTestCase, SetUpSignedInClient
from django.utils.translation import gettext_lazy as _


class UnavailableForGuestsTestCase(SetUpTestCase):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('status_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('status_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('status_index'), follow=True)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(
            response,
            _('This can be done only by an authenticated user!'))


class CRUDTestCase(SetUpSignedInClient):

    def test_create(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, 'created_status')

        response = self.client.post(
            reverse_lazy('status_create'),
            {'name': 'created_status'}, follow=True)
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.assertContains(response, _('Status created successfully'))

        response = self.client.get(reverse_lazy('status_index'))
        self.assertContains(response, 'created_status')

    def test_setup(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertContains(response, self.unused_status.name)

    def test_delete(self):
        response = self.client.post(
            reverse_lazy(
                'status_delete',
                kwargs={'pk': self.unused_status.pk}),
            follow=True)
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.assertContains(response, _('The status was deleted'))

        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, self.unused_status.name)

    def test_update(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, 'renamed_status')

        response = self.client.post(
            reverse_lazy('status_update',
                         kwargs={'pk': self.unused_status.pk}),
            {'name': 'renamed_status'}, follow=True)
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.assertContains(response, _('The status was updated'))

        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, self.unused_status.name)
        self.assertContains(response, 'renamed_status')

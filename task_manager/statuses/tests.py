from django.urls import reverse_lazy
from task_manager.utils import (
    SetUpTestCase, SetUpSignedInClient, CheckFlashMixin
)


class UnavailableForGuestsTestCase(SetUpTestCase, CheckFlashMixin):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('status_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('status_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertRedirects(response, reverse_lazy('login'))
        self.check_flash(response,
                         'This can be done only by an authenticated user!')


class CRUDTestCase(SetUpSignedInClient, CheckFlashMixin):

    def test_create(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, 'created_status')

        response = self.client.post(reverse_lazy('status_create'),
                                    {'name': 'created_status'})
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.check_flash(response, 'Status created successfully')

        response = self.client.get(reverse_lazy('status_index'))
        self.assertContains(response, 'created_status')

    def test_setup(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertContains(response, self.unused_status.name)

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('status_delete',
                         kwargs={'pk': self.unused_status.pk}))
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.check_flash(response, "The status was deleted")

        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, self.unused_status.name)

    def test_update(self):
        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, 'renamed_status')

        response = self.client.post(
            reverse_lazy('status_update',
                         kwargs={'pk': self.unused_status.pk}),
            {'name': 'renamed_status'})
        self.assertRedirects(response, reverse_lazy('status_index'))
        self.check_flash(response, "The status was updated")

        response = self.client.get(reverse_lazy('status_index'))
        self.assertNotContains(response, self.unused_status.name)
        self.assertContains(response, 'renamed_status')

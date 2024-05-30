from django.urls import reverse_lazy
from task_manager.utils import (
    SetUpTestCase, SetUpSignedInClient, CheckFlashMixin
)


class UnavailableForGuestsTestCase(SetUpTestCase, CheckFlashMixin):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('label_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('label_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertRedirects(response, reverse_lazy('login'))
        self.check_flash(response,
                         'This can be done only by an authenticated user!')


class CRUDTestCase(SetUpSignedInClient, CheckFlashMixin):

    def test_create(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, 'created_label')

        response = self.client.post(reverse_lazy('label_create'),
                                    {'name': 'created_label'})
        self.assertRedirects(response, reverse_lazy('label_index'))
        self.check_flash(response, 'Label created successfully')

        response = self.client.get(reverse_lazy('label_index'))
        self.assertContains(response, 'created_label')

    def test_setup(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertContains(response, self.unused_label.name)

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': self.unused_label.pk}))
        self.assertRedirects(response, reverse_lazy('label_index'))
        self.check_flash(response, "The label was deleted")

        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, self.unused_label.name)

    def test_update(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, 'renamed_label')

        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': self.unused_label.pk}),
            {'name': 'renamed_label'})
        self.assertRedirects(response, reverse_lazy('label_index'))
        self.check_flash(response, "The label was updated")

        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, self.unused_label.name)
        self.assertContains(response, 'renamed_label')

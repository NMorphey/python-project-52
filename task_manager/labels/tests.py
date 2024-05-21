from django.urls import reverse_lazy
from task_manager.utils import SetUpUsers, SetUpLabel


class UnavailableForGuestsTestCase(SetUpUsers):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('label_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('label_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertEqual(response.status_code, 302)


class CRUDTestCase(SetUpLabel):

    def test_create(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, 'created_label')

        self.client.post(reverse_lazy('label_create'),
                         {'name': 'created_label'})

        response = self.client.get(reverse_lazy('label_index'))
        self.assertContains(response, 'created_label')

    def test_setup(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertContains(response, self.label_name)

    def test_delete(self):
        self.client.post(reverse_lazy('label_delete', kwargs={'pk': 1}))
        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, self.label_name)

    def test_update(self):
        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, 'renamed_label')

        self.client.post(reverse_lazy('label_update', kwargs={'pk': 1}),
                         {'name': 'renamed_label'})

        response = self.client.get(reverse_lazy('label_index'))
        self.assertNotContains(response, self.label_name)
        self.assertContains(response, 'renamed_label')

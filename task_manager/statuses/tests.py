from django.urls import reverse_lazy
from task_manager.utils import SetUpUsers, SetUpSignedInClient


class SetUpStatus(SetUpSignedInClient):

    def setUp(self):
        super().setUp()
        self.status_name = 'test_status'
        self.client.post(reverse_lazy('create_status'), {'name': self.status_name})


class UnavailableForGuestsTestCase(SetUpUsers):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('statuses_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('statuses_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertEqual(response.status_code, 302)


class CRUDTestCase(SetUpStatus):

    def test_create(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertNotContains(response, 'created_status')

        self.client.post(reverse_lazy('create_status'), {'name': 'created_status'})

        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertContains(response, 'created_status')

    def test_setup(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertContains(response, self.status_name)

    def test_delete(self):
        self.client.post(reverse_lazy('delete_status', kwargs={'pk': 1}))
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertNotContains(response, self.status_name)

    def test_update(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertNotContains(response, 'renamed_status')

        self.client.post(reverse_lazy('update_status', kwargs={'pk': 1}), {'name': 'renamed_status'})

        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertNotContains(response, self.status_name)
        self.assertContains(response, 'renamed_status')

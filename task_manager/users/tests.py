from django.urls import reverse_lazy
from task_manager.utils import SetUpClient, SetUpUsers


class GuestUserTestCase(SetUpClient):

    def test_users_index_avalable(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)

    def test_signup_and_singin_avalable(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)


class CRUDTestCase(SetUpUsers):

    def test_set_up(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'User Testov')

    def test_allowed_to_sign_in(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, 'action="/logout/"')

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, 'action="/logout/"')

    def test_users_are_allowed_to_update_and_delete_only_themselves(self):
        # Signing in as pk-1 user
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        response = self.client.get(
            reverse_lazy('update_user', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse_lazy('delete_user', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)

        update_data = self.user_1_data
        update_data['username'] = 'some_new_username'
        self.client.post(
            reverse_lazy('update_user', kwargs={'pk': 2}), update_data
        )
        self.client.post(reverse_lazy('delete_user', kwargs={'pk': 2}))
        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'another_user')
        self.assertNotContains(response, 'some_new_username')

        response = self.client.get(
            reverse_lazy('update_user', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse_lazy('delete_user', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        update_data = self.user_1_data
        update_data['first_name'] = 'Updated'
        self.client.post(
            reverse_lazy('update_user', kwargs={'pk': 1}), update_data
        )

        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'Updated Testov')
        self.assertNotContains(response, 'User Testov')

    def test_delete(self):
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        self.client.post(reverse_lazy('delete_user', kwargs={'pk': 1}))
        response = self.client.get(reverse_lazy('users_index'))
        self.assertNotContains(response, 'User Testov')

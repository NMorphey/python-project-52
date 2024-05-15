from django.test import TestCase, Client
from django.urls import reverse_lazy


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

        user_2_data = {
            'first_name': 'User',
            'last_name': 'Another',
            'username': 'another_user',
            'password1': 'qwerty',
            'password2': 'qwerty'
        }
        self.client.post(reverse_lazy('registration'), user_2_data)


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

    def test_sign_up(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'User Testov')

    def test_allowed_to_sign_in(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, 'action="/logout/"')

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, 'action="/logout/"')

    def test_users_are_allowed_to_update_and_delete_only_themselves(self):
        # Signing in as id-1 user
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        response = self.client.get(reverse_lazy('update_user', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('delete_user', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 302)

        update_data = self.user_1_data
        update_data['username'] = 'some_new_username'
        self.client.post(reverse_lazy('update_user', kwargs={'id': 2}), update_data)
        self.client.post(reverse_lazy('delete_user', kwargs={'id': 2}))
        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'another_user')
        self.assertNotContains(response, 'some_new_username')

        response = self.client.get(reverse_lazy('update_user', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse_lazy('delete_user', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        update_data = self.user_1_data
        update_data['first_name'] = 'Updated'
        self.client.post(reverse_lazy('update_user', kwargs={'id': 1}), update_data)

        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'Updated Testov')
        self.assertNotContains(response, 'User Testov')

    def test_delete(self):
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        self.client.post(reverse_lazy('delete_user', kwargs={'id': 1}))
        response = self.client.get(reverse_lazy('users_index'))
        self.assertNotContains(response, 'User Testov')

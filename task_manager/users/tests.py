from django.urls import reverse_lazy
from task_manager.utils import SetUpTestCase, CheckFlashMixin
from django.test import TestCase


class GuestUserTestCase(TestCase):

    def test_users_index_avalable(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)

    def test_signup_and_singin_avalable(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)


class CRUDTestCase(SetUpTestCase, CheckFlashMixin):

    def test_registration(self):
        response = self.client.post(reverse_lazy('registration'), {
            'first_name': 'first',
            'last_name': 'last',
            'username': '123',
            'password1': '123',
            'password2': '123'
        })
        self.assertRedirects(response, reverse_lazy('login'))
        self.check_flash(response, 'The user created successfully')

    def test_set_up(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'User Testov')

    def test_allowed_to_sign_in(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('logout'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('logout'))
        self.check_flash(response, 'Logged in successfully')

    def task_cannot_delete_other_users(self):
        # Signing in as pk-1 user
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        response = self.client.get(
            reverse_lazy('delete_user', kwargs={'pk': 2})
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response,
                         'You are not authorized to modify other users.')

        response = self.client.post(
            reverse_lazy('delete_user', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response,
                         'You are not authorized to modify other users.')

        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'another_user')

    def test_cannot_update_other_users(self):
        # Signing in as pk-1 user
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        response = self.client.get(
            reverse_lazy('update_user', kwargs={'pk': 2})
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response,
                         'You are not authorized to modify other users.')

        update_data = {
            'first_name': self.user_2.first_name,
            'last_name': self.user_2.last_name,
            'username': self.user_2.username,
            'password1': self.user_2_login_data['password'],
            'password2': self.user_2_login_data['password']
        }
        response = self.client.post(
            reverse_lazy('update_user', kwargs={'pk': 2}), update_data
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response,
                         'You are not authorized to modify other users.')

        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'another_user')
        self.assertNotContains(response, 'some_new_username')

    def test_update(self):
        self.client.post(reverse_lazy('login'), self.user_1_login_data)

        update_data = {
            'first_name': 'Updated',
            'last_name': self.user_1.last_name,
            'username': self.user_1.username,
            'password1': self.user_1_login_data['password'],
            'password2': self.user_1_login_data['password']
        }
        response = self.client.post(
            reverse_lazy('update_user', kwargs={'pk': 1}), update_data
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response, 'User updated successfully')

        response = self.client.get(reverse_lazy('users_index'))
        self.assertContains(response, 'Updated Testov')
        self.assertNotContains(response, 'User Testov')

    def test_delete(self):
        self.client.post(reverse_lazy('login'), self.user_3_login_data)

        response = self.client.post(
            reverse_lazy('delete_user', kwargs={'pk': 3}))
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.check_flash(response, 'User deleted successfully')

        response = self.client.get(reverse_lazy('users_index'))
        self.assertNotContains(response, self.user_3.get_full_name)

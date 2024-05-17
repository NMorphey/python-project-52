from django.urls import reverse_lazy
from task_manager.utils import SetUpUsers, SetUpStatus


class UnavailableForGuestsTestCase(SetUpUsers):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('tasks_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('tasks_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertEqual(response.status_code, 302)


class SetUpTask(SetUpStatus):

    def setUp(self):
        super().setUp()
        self.task_name = 'test_task'
        self.client.post(reverse_lazy('create_task'),
                         {'name': self.task_name, 'status': 1})


class CRUDTestCase(SetUpTask):

    def test_create(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertNotContains(response, 'created_task')

        self.client.post(reverse_lazy('create_task'),
                         {'name': 'created_task', 'status': 1})

        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertContains(response, 'created_task')

    def test_setup(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertContains(response, self.task_name)

    def test_delete(self):
        self.client.post(reverse_lazy('delete_task', kwargs={'pk': 1}))
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertNotContains(response, self.task_name)

    def test_update(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertNotContains(response, 'renamed_task')

        self.client.post(reverse_lazy('update_task', kwargs={'pk': 1}),
                         {'name': 'renamed_task', 'status': 1})

        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertNotContains(response, self.task_name)
        self.assertContains(response, 'renamed_task')

from django.urls import reverse_lazy
from task_manager.utils import SetUpUsers, SetUpStatus


class UnavailableForGuestsTestCase(SetUpUsers):

    def test_category_on_main_page(self):
        response = self.client.get(reverse_lazy('main_page'))
        self.assertNotContains(response, reverse_lazy('task_index'))

        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        response = self.client.get(reverse_lazy('main_page'))
        self.assertContains(response, reverse_lazy('task_index'))

    def test_redirects(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertEqual(response.status_code, 302)


class SetUpTask(SetUpStatus):

    def setUp(self):
        super().setUp()
        self.task_name = 'test_task'
        self.client.post(reverse_lazy('task_create'),
                         {'name': self.task_name, 'status': 1})


class CRUDTestCase(SetUpTask):

    def test_create(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, 'created_task')

        self.client.post(reverse_lazy('task_create'),
                         {'name': 'created_task', 'status': 1})

        response = self.client.get(reverse_lazy('task_index'))
        self.assertContains(response, 'created_task')

    def test_setup(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertContains(response, self.task_name)

    def test_delete(self):
        self.client.post(reverse_lazy('task_delete', kwargs={'pk': 1}))
        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, self.task_name)

    def test_update(self):
        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, 'renamed_task')

        self.client.post(reverse_lazy('task_update', kwargs={'pk': 1}),
                         {'name': 'renamed_task', 'status': 1})

        response = self.client.get(reverse_lazy('task_index'))
        self.assertNotContains(response, self.task_name)
        self.assertContains(response, 'renamed_task')


class QueryTestCase(SetUpUsers):

    def setUp(self):
        super().setUp()
        # Login as user 1
        self.client.post(reverse_lazy('login'), self.user_1_login_data)
        # Setup statuses
        self.client.post(reverse_lazy('status_create'), {'name': 'status1'})
        self.client.post(reverse_lazy('status_create'), {'name': 'status2'})
        # Setup labels
        self.client.post(reverse_lazy('label_create'), {'name': 'label1'})
        self.client.post(reverse_lazy('label_create'), {'name': 'label2'})
        self.client.post(reverse_lazy('label_create'), {'name': 'label3'})
        # Create tasks as user 1
        self.client.post(reverse_lazy('task_create'), {
            'name': 'task1',
            'status': 1,
            'executor': 2,
            'labels': [1, 2]
        })
        self.client.post(reverse_lazy('task_create'), {
            'name': 'task2',
            'status': 2,
            'executor': 1,
            'labels': [1]
        })
        # Login as user 2
        self.client.post(reverse_lazy('logout'))
        self.client.post(reverse_lazy('login'), self.user_2_login_data)
        # Create task as user 2
        self.client.post(reverse_lazy('task_create'), {
            'name': 'task3',
            'status': 1,
            'executor': 1,
            'labels': [1, 2]
        })
        # Client stays logged in as user 2

    def test_status_search(self):
        response = self.client.get(reverse_lazy('task_index'), {'status': 1})
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')

    def test_executor_search(self):
        response = self.client.get(reverse_lazy('task_index'),
                                   {'executor': 1})
        self.assertNotContains(response, 'task1')
        self.assertContains(response, 'task2')
        self.assertContains(response, 'task3')

    def test_self_search(self):
        response = self.client.get(reverse_lazy('task_index'),
                                   {'self_tasks': 'on'})
        self.assertNotContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')

    def test_lables_search(self):
        response = self.client.get(reverse_lazy('task_index'), {'label': 1})
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')
        self.assertContains(response, 'task3')

        response = self.client.get(reverse_lazy('task_index'), {'label': 2})
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')

        response = self.client.get(reverse_lazy('task_index'), {'label': 3})
        self.assertNotContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertNotContains(response, 'task3')

    def test_multiple_searches(self):
        response = self.client.get(
            reverse_lazy('task_index'),
            {'label': 1, 'self_tasks': 'on', 'executor': 1, 'status': 1}
        )
        self.assertNotContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')

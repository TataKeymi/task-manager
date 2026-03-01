from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        position = Position.objects.create(name="test")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
            position=position
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=position,
        )


    def test_worker_position_listed(self):
        """
        Tests that worker`s position is listed in the worker list page.
        :return:
        """
        url = reverse("admin:tasks_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        """
        Tests that worker`s position is listed in the worker detail page.
        :return:
        """
        url = reverse("admin:tasks_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_add_position_listed(self):
        """
        Tests that worker`s position is listed in the worker adding page.
        :return:
        """
        url = reverse("admin:tasks_worker_add")
        res = self.client.get(url)
        self.assertContains(res, 'name="position"')
        self.assertContains(res, 'name="first_name"')
        self.assertContains(res, 'name="last_name"')
        self.assertContains(res, 'name="email"')

    def test_worker_position_filter_works(self):
        """
        Tests that workers are correctly filtered by position.
        :return:
        """
        first_position = Position.objects.create(name="first")
        second_position = Position.objects.create(name="second")
        first_worker = get_user_model().objects.create_user(
            username="first_worker",
            password="testfirst",
            position=first_position,
        )
        second_worker = get_user_model().objects.create_user(
            username="second_worker",
            password="testsecond",
            position=second_position,
        )
        url = reverse("admin:tasks_worker_changelist")
        res = self.client.get(url, {"position": second_position.id})
        self.assertContains(res, second_worker.username)
        self.assertNotContains(res, first_worker.username)

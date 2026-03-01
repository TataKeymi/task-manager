from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import TaskType, Project, Team, Task, Position, Worker, Tag

TASK_URL = reverse("tasks:task-list")
WORKER_URL = reverse("tasks:worker-list")
POSITION_URL = reverse("tasks:position-list")
TASK_TYPE_URL = reverse("tasks:task-type-list")
TAG_URL = reverse("tasks:tag-list")
PROJECT_URL = reverse("tasks:project-list")
TEAM_URL = reverse("tasks:team-list")


class PublicTaskTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_tasks(self):
        task_type = TaskType.objects.create(name="test")
        team = Team.objects.create(name="test")
        project = Project.objects.create(name="test", team=team)
        Task.objects.create(name="first test", task_type=task_type, project=project)
        Task.objects.create(name="second test", task_type=task_type, project=project)
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Task.objects.all())
        self.assertTemplateUsed(res, "tasks/task_list.html")
        res = self.client.get(TASK_URL,{"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Task.objects.filter(name__icontains="first"))


class PublicWorkerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        position = Position.objects.create(name="test_position")
        Worker.objects.create(username="first_test", position=position)
        Worker.objects.create(username="second_test", position=position)
        res = self.client.get(WORKER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Worker.objects.all())
        self.assertTemplateUsed(res, "tasks/worker_list.html")
        res = self.client.get(WORKER_URL,{"username": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Worker.objects.filter(username__icontains="first"))

    def test_create_worker(self):
        position = Position.objects.create(name="testpos")
        form_data = {
            "username": "test_user",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "first",
            "last_name": "last",
            "email": "test@user.com",
            "position": position.id,
        }
        self.client.post(reverse("tasks:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.email, form_data["email"])
        self.assertEqual(new_user.position, position)


class PublicPositionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)

class PrivatePositionTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        Position.objects.create(name="first_position")
        Position.objects.create(name="second_position")
        res = self.client.get(POSITION_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Position.objects.all())
        self.assertTemplateUsed(res, "tasks/position_list.html")
        res = self.client.get(POSITION_URL, {"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Position.objects.filter(name__icontains="first"))


class PublicTaskTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="first test")
        TaskType.objects.create(name="second test")
        res = self.client.get(TASK_TYPE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], TaskType.objects.all())
        self.assertTemplateUsed(res, "tasks/task_type_list.html")
        res = self.client.get(TASK_TYPE_URL, {"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], TaskType.objects.filter(name__icontains="first"))


class PublicTagTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TAG_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTagTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(name="first test")
        Tag.objects.create(name="second test")
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Tag.objects.all())
        self.assertTemplateUsed(res, "tasks/tag_list.html")
        res = self.client.get(TAG_URL, {"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Tag.objects.filter(name__icontains="first"))


class PublicProjectTest(TestCase):
    def test_login_required(self):
        res = self.client.get(PROJECT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateProjectTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_projects(self):
        team = Team.objects.create(name="test")
        Project.objects.create(name="first test", team=team)
        Project.objects.create(name="second test", team=team)
        res = self.client.get(PROJECT_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Project.objects.all())
        self.assertTemplateUsed(res, "tasks/project_list.html")
        res = self.client.get(PROJECT_URL, {"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Project.objects.filter(name__icontains="first"))


class PublicTeamTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TEAM_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTeamTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_teams(self):
        Team.objects.create(name="first test")
        Team.objects.create(name="second test")
        res = self.client.get(TEAM_URL)
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["object_list"], Team.objects.all())
        self.assertTemplateUsed(res, "tasks/team_list.html")
        res = self.client.get(TEAM_URL, {"name": "first"})
        self.assertQuerysetEqual(res.context["object_list"], Team.objects.filter(name__icontains="first"))

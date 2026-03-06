import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.models import Position, Worker, TaskType, Tag, Team, Project, Task, TaskPriority


class ModelTests(TestCase):
    def test_position_str(self):
        position = Position(name="test_position")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        position = Position.objects.create(name="test_position")
        worker = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position
        )
        self.assertEqual(str(worker), f"{worker.username}: {worker.first_name} {worker.last_name}")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        self.assertEqual(str(task_type), task_type.name)

    def test_tag_str(self):
        tag = Tag.objects.create(name="test_tag")
        self.assertEqual(str(tag), tag.name)

    def test_team_str(self):
        team = Team.objects.create(name="test_team")
        self.assertEqual(str(team), team.name)

    def test_project_str(self):
        team = Team.objects.create(name="test_team")
        project = Project.objects.create(name="test_project", team=team)
        self.assertEqual(str(project), project.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        team = Team.objects.create(name="test_team")
        project = Project.objects.create(name="test_project", team=team)
        task = Task.objects.create(
            name="test_task",
            task_type=task_type,
            project=project,
            deadline=datetime.datetime.now(),
            priority=TaskPriority.MEDIUM
        )
        self.assertEqual(str(task), f"{task.name}: till {task.deadline}, priority {task.priority}")

    def test_create_worker_with_position(self):
        position = Position.objects.create(name="test_position")
        worker = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position
        )
        self.assertEqual(worker.username, "test_username")
        self.assertEqual(worker.position, position)

    def test_position_worker_count(self):
        position = Position.objects.create(name="test_position")
        get_user_model().objects.create(
            username="test_first_username",
            position=position
        )
        get_user_model().objects.create(
            username="test_second_username",
            position=position
        )
        self.assertEqual(position.worker_count, 2)

    def test_task_type_task_count(self):
        task_type = TaskType.objects.create(name="test_task_type")
        team = Team.objects.create(name="test_team")
        project = Project.objects.create(name="test_project", team=team)
        Task.objects.create(
            name="test_task_first",
            task_type=task_type,
            project=project,
        )
        Task.objects.create(
            name="test_task_second",
            task_type=task_type,
            project=project,
        )
        self.assertEqual(task_type.task_count, 2)

    def test_tag_task_count(self):
        tag = Tag.objects.create(name="test_tag")
        task_type = TaskType.objects.create(name="test_task_type")
        team = Team.objects.create(name="test_team")
        project = Project.objects.create(name="test_project", team=team)
        first_task = Task.objects.create(
            name="test_task_first",
            task_type=task_type,
            project=project,
        )
        second_task = Task.objects.create(
            name="test_task_second",
            task_type=task_type,
            project=project,
        )
        first_task.tags.add(tag)
        second_task.tags.add(tag)
        self.assertEqual(tag.task_count, 2)

    def test_task_is_overdue(self):
        task_type = TaskType.objects.create(name="test_task_type")
        team = Team.objects.create(name="test_team")
        project = Project.objects.create(name="test_project", team=team)
        task = Task.objects.create(
            name="test_task",
            task_type=task_type,
            project=project,
            deadline=timezone.now().date() - timezone.timedelta(days=14)
        )
        self.assertTrue(task.is_overdue())

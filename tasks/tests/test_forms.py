from django.test import TestCase

from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Project, TaskType, Team, TaskPriority


class FormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="test task type")
        self.team = Team.objects.create(name="test team")
        self.project = Project.objects.create(name="test project", team=self.team)

    def test_task_deadline_can_not_be_in_the_past(self):
        form_date = {
            "name": "test task",
            "description": "test task description",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "deadline": timezone.now().date() - timezone.timedelta(days=1),
            "priority": TaskPriority.MEDIUM
        }
        form = TaskForm(data=form_date)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_task_deadline_can_be_in_the_future_and_present(self):
        form_date = {
            "name": "test task",
            "description": "test task description",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "deadline": timezone.now().date() + timezone.timedelta(days=1),
            "priority": TaskPriority.MEDIUM
        }
        form = TaskForm(data=form_date)
        self.assertTrue(form.is_valid())
        form_date = {
            "name": "test task",
            "description": "test task description",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "deadline": timezone.now().date(),
            "priority": TaskPriority.MEDIUM
        }
        form = TaskForm(data=form_date)
        self.assertTrue(form.is_valid())

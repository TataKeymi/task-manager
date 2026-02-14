from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager import settings


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def worker_count(self):
        return self.workers.count()


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        default="Unknown",
        related_name="workers",)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"



class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaskPriority(models.TextChoices):  # class for priority field in Task model
    URGENT = "urgent", "Urgent"
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM)
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return f"{self.name}: {self.get_priority_display()}"

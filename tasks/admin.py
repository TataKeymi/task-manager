from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Task, TaskType, Worker, Position, Tag, Team, Project


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed", "priority", "task_type", "get_assignees", "project"]
    list_filter = ["deadline", "is_completed", "priority", "task_type", "project"]
    search_fields = ["name", "description"]

    @admin.display(description="assignees")
    def get_assignees(self, obj):
        return ",".join(obj.assignees.values_list("username", flat=True))


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("first_name", "last_name", "email", "position",)}),)
    list_filter = UserAdmin.list_filter + ("position",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ["name",]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name",]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name",]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ["name",]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["name",]


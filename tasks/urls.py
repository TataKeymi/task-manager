from django.urls import path

from tasks.views import (index,
                         TaskListView,
                         WorkerListView,
                         TaskDetailView,
                         TaskCreateView,
                         TaskUpdateView,
                         TaskDeleteView,
                         WorkerDetailView,
                         WorkerDeleteView,
                         WorkerCreateView,
                         PositionListView,
                         PositionDetailView,
                         PositionCreateView,
                         PositionUpdateView)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/update/<int:pk>", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/delete/<int:pk>", TaskDeleteView.as_view(), name="task-delete"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),

    path("workers/delete/<int:pk>", WorkerDeleteView.as_view(), name="worker-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>", PositionDetailView.as_view(), name="position-detail"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/update/<int:pk>", PositionUpdateView.as_view(), name="position-update"),
]

app_name = "tasks"

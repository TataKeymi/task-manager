from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (TaskForm,
                         WorkerCreationForm,
                         TaskSearchForm,
                         WorkerSearchForm,
                         PositionSearchForm,
                         TaskTypeSearchForm, TagSearchForm, ProjectSearchForm, TeamSearchForm)
from tasks.models import Task, Worker, Position, TaskType, Tag, Project, Team


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_visits": num_visits + 1,
    }

    return render(request, "tasks/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.prefetch_related("assignees")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = TaskSearchForm(
            initial={"name": name},
        )
        return context

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")
    success_message = "Task successfully created"


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")
    success_message = "Task successfully updated"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")

    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Task successfully deleted")
        return response

class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["username"] = username
        context["search_form"] = WorkerSearchForm(
            initial={"username": username},
        )
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incompleted_tasks"] = self.object.tasks.filter(is_completed=False)
        context["completed_tasks"] = self.object.tasks.filter(is_completed=True)
        return context



class WorkerCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")
    success_message = "Worker successfully created"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")

    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Worker successfully deleted")
        return response


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = PositionSearchForm(
            initial={"name": name},
        )
        return context


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Position
    fields = ("name",)
    success_url = reverse_lazy("tasks:position-list")
    success_message = "Position successfully updated."


class PositionUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Position
    fields = ("name",)
    success_url = reverse_lazy("tasks:position-list")
    success_message = "Position successfully updated"


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 10
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name},
        )
        return context


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "tasks/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = TaskType
    fields = ("name",)
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_form.html"
    context_object_name = "task_type"
    success_message = "Task type successfully created."



class TaskTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = TaskType
    fields = ("name",)
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_form.html"
    context_object_name = "task_type"
    success_message = "Task type successfully updated."



class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10

    def get_queryset(self):
        queryset = Tag.objects.all()
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = TagSearchForm(
            initial={"name": name},
        )
        return context


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag


class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Tag
    fields = ("name",)
    success_url = reverse_lazy("tasks:tag-list")
    success_message = "Tag successfully created."


class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Tag
    fields = ("name",)
    success_url = reverse_lazy("tasks:tag-list")
    success_message = "Tag successfully updated."


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")

    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Tag successfully deleted.")
        return response


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = ProjectSearchForm(
            initial={"name": name},
        )
        return context


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Project
    fields = ("name", "team",)
    success_url = reverse_lazy("tasks:project-list")
    success_message = "Project successfully created."


class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Project
    fields = ("name","team", )
    success_url = reverse_lazy("tasks:project-list")
    success_message = "Project successfully updated."


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:project-list")

    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Project successfully deleted.")
        return response


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 10

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["name"] = name
        context["search_form"] = TeamSearchForm(
            initial={"name": name},
        )
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Team
    fields = ("name", "workers",)
    success_url = reverse_lazy("tasks:team-list")
    success_message = "Team successfully created."


class TeamUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Team
    fields = ("name", "workers",)
    success_url = reverse_lazy("tasks:team-list")
    success_message = "Team successfully updated."


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")

    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Team successfully deleted.")
        return response


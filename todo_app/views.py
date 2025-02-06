from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Task, SubTask, Comment, Team, TeamMembership, Invitation
from .forms import TaskForm, CommentForm,TeamCreateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# # Rest API
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import viewsets

# from .serializers import TaskSerializer


# -------------------
# User Registration View
# -------------------
def register(request):
    """
    Handle user registration. If the request method is POST, validate the form
    and create a new user. If valid, log the user in and redirect to the task list.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in
            messages.success(
                request, "Registration successful! Welcome."
            )  # Success message
            return redirect("task_list")  # Redirect to the task list
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = UserCreationForm()  # Render an empty form for GET request

    return render(request, "todo_app/register.html", {"form": form})


# -------------------
# User Login View
# -------------------
def user_login(request):
    """
    Handle user login. If the request method is POST, authenticate the user.
    If valid, log the user in and redirect to the task list.
    """
    if request.method == "POST":
        form = AuthenticationForm(
            request, data=request.POST
        )  # Bind form with POST data
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request, username=username, password=password
            )  # Authenticate user

            if user is not None:
                login(request, user)  # Log the user in
                messages.success(
                    request, f"Welcome back, {user.username}!"
                )  # Success message
                return redirect("task_list")  # Redirect to task list
            else:
                messages.error(
                    request, "Invalid username or password."
                )  # Error message
        else:
            messages.error(
                request, form.non_field_errors()
            )  # Handle general form errors
    else:
        form = AuthenticationForm()  # Render an empty form for GET request

    return render(request, "todo_app/login.html", {"form": form})


# -------------------
# User Logout View
# -------------------
def logout_view(request):
    """
    Log the user out and redirect to the login page with a success message.
    """
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out.")  # Success message
    return redirect("login")  # Redirect to login page


# -------------------
# Task List View
# -------------------
@login_required
def task_list(request):
    """
    Display a list of tasks belonging to the currently logged-in user.
    """
    tasks = Task.objects.filter(team__members=request.user)  # Get tasks for the logged-in user
    return render(request, "todo_app/task_list.html", {"tasks": tasks})


# -------------------
# Task Create View
# -------------------
@login_required
def task_create(request):
    """
    Handle the creation of a new task. If valid, save the task and redirect to task list.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)  # Bind form with POST data
        if form.is_valid():
            task = form.save(commit=False)  # Don't save to DB yet
            task.user = request.user  # Assign the current user to the task
            task.save()  # Save the task to the database
            form.save_m2m()
            messages.success(request, "Task created successfully!")  # Success message
            return redirect("task_list")      # Redirect to task list
        else:
            messages.error(
                request, "Failed to create task. Please fix the errors below."
            )  # Error message
    else:
        form = TaskForm()  # Render an empty form for GET request

    return render(request, "todo_app/task_form.html", {"form": form})


# categroies = [1, 2, 3]


# -------------------
# Task Update View
# -------------------
@login_required
def task_update(request, pk):
    """
    Handle updating an existing task. If valid, save the task and redirect to the task list.
    """
    task = get_object_or_404(Task, pk=pk)  # Get the task or return 404 if not found
    if request.method == "POST":
        form = TaskForm(
            request.POST, instance=task
        )  # Bind form with POST data and existing instance
        if form.is_valid():
            form.save()  # Save the updated task
            messages.success(request, "Task updated successfully!")  # Success message
            return redirect("task_list")  # Redirect to task list
        else:
            messages.error(
                request, "Failed to update task. Please fix the errors below."
            )  # Error message
    else:
        form = TaskForm(instance=task)  # Prepopulate form with existing task data

    return render(request, "todo_app/task_form.html", {"form": form})


# -------------------
# Task Delete View
# -------------------
@login_required
def task_delete(request, pk):
    """
    Handle deleting a task. Confirm deletion before proceeding.
    """
    task = get_object_or_404(Task, pk=pk)  # Get the task or return 404 if not found
    if request.method == "POST":
        task.delete()  # Delete the task from the database
        messages.success(request, "Task deleted successfully!")  # Success message
        return redirect("task_list")  # Redirect to task list

    return render(request, "todo_app/task_confirm_delete.html", {"task": task})


    # -------------------
    # Task Detail View
    # -------------------
@login_required
# Task Detail View with Comments
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    comments = task.comments.filter(parent__isnull=True).order_by(
        "-created_at"
    )  # Only top-level comments
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            parent_id = request.POST.get(
                "parent_id"
            )  # Check if there's a parent ID for a     
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect("task_detail", pk=task.id)
    else:
        form = CommentForm()

    context = {
        "task": task,
        "comments": comments,
        "form": form,
    }
    return render(request, "todo_app/task_detail.html", context)


# -------------------
# Subtask Create View
# -------------------
@login_required
def subtask_create(request, task_pk):
    """
    Handle the creation of a subtask for a specific task.
    """
    task = get_object_or_404(
        Task, pk=task_pk, user=request.user
    )  # Get the parent task or return 404
    if request.method == "POST":
        title = request.POST.get("title")  # Get the title from POST data
        completed = (
            request.POST.get("completed") == "on"
        )  # Handle checkbox for completion

        SubTask.objects.create(
            title=title, completed=completed, task=task
        )  # Create and save the subtask
        messages.success(request, "Subtask added successfully!")  # Success message
        return redirect("task_detail", pk=task_pk)  # Redirect back to task detail

    messages.error(request, "Failed to create subtask.")  # Error message
    return redirect("task_detail", pk=task_pk)  # Redirect back to task detail

# ---------------------------------------------------------
# Team Invitation Views
# ---------------------------------------------------------
@login_required
def invite_to_team(request,team_id):
    team = get_object_or_404(Team,id=team_id)
    if request.method == "POST":
        invited_user_id = request.POST.get("invited_user_id")
        invited_user = get_object_or_404(User,id=invited_user_id)
        Invitation.objects.create(
            team=team, invited_user=invited_user, sender=request.user
        )
        messages.success(request,f"Invitation sent to {invited_user.username}.")
        return redirect("team_list",team_id=team.id)

    users_to_invite = User.objects.exclude(teams=team)
    return render(
        request,
        "todo_app/invite_to_team.html",
        {"team":team,"users":users_to_invite},
    )


# -------------------
# View Invitations
# -------------------

@login_required
def view_invitaitions(request):
    invitations = request.user.invitations_received.filter(accepted = False)
    return render(request,"todo_app/invitations.html",{"invitations":invitations})

# -------------------
# Accept or Decline Invitation
# -------------------

@login_required
def respond_to_invitation(request,invitation_id,response):
    invitation = get_object_or_404(
        Invitation, id=invitation_id, invited_user = request.user
    )

    if response == "accept":
        invitation.accepted = True
        invitation.save()
        TeamMembership.objects.create(user=request.user,team=invitation.team)
        messages.success(request,f"You have joined the team {invitation.team.name}!")
    elif response == "decline":
        invitation.delete()
        messages.info(request,"Invitation declined.")
    return redirect("view_invitations")


# ---------------------------------------------------------
# Team Create Views
# ---------------------------------------------------------

@login_required
def team_list(request):
    teams = request.user.teams.all()
    return render(request,"todo_app/team_list.html",{"teams":teams})

@login_required
def team_create(request):
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            TeamMembership.objects.create(user=request.user,team=team)
            messages.success(request,f'Team "{team.name}" created successfully!')
            return redirect("task_list")
        else:
            messages.error(
                request,"Failed to create team. Please correct the errors below"
            )
    else:
        form = TeamCreateForm()
    
    return render(request,"todo_app/team_create.html",{"form":form})


# ---------------------------------------------------------
# Class Based Views
# ---------------------------------------------------------
"""from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


# Task List View
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo_app/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# Task Detail View
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "todo_app/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtasks"] = self.object.subtasks.all()  # Fetch subtasks
        return context


# Task Create View
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


# Task Update View
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy("task_list")


# Task Delete View
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "todo_app/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")


# Subtask Create View
class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    fields = ["title", "completed"]
    template_name = "todo_app/subtask_form.html"

    def form_valid(self, form):
        task = get_object_or_404(
            Task, pk=self.kwargs["task_pk"], user=self.request.user
        )
        form.instance.task = task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.kwargs["task_pk"]})


# User Registration View
class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "todo_app/register.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log the user in after registration
        return super().form_valid(form)


# User Login View
class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "todo_app/login.html"

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


# User Logout View
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")"""


# ---------------------------------------------------------
# REST API's Based Views
# ---------------------------------------------------------

# # List view - Retrieve all tasks
# class TaskListAPIView(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)


# # Create view - Create a new task
# class TaskCreateAPIView(APIView):
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Update view - Update an existing task
# class TaskUpdateAPIView(APIView):
#     def put(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Delete view - Delete a task
# class TaskDeleteAPIView(APIView):
#     def delete(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # Easy Method for all CRUD Endpoints in REST API
# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

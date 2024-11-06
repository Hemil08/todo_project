from django.urls import path, include
from . import views

# # REST API
# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet

# REST API
# router = DefaultRouter()
# router.register(r"tasks", TaskViewSet)
# /accounts/login/
# /accounts/register/
# /accounts/logout/


urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),  # New detail view
    path("task/create/", views.task_create, name="task_create"),
    path("task/<int:pk>/update/", views.task_update, name="task_update"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path(
        "task/<int:task_pk>/subtask/create/",
        views.subtask_create,
        name="subtask_create",
    ),
    # path("", views.TaskListAPIView.as_view(), name="task_list"),
    # path("create/", views.TaskCreateAPIView.as_view(), name="task_create"),
    # path("update/<int:pk>/", views.TaskUpdateAPIView.as_view(), name="task_update"),
    # path("delete/<int:pk>/", views.TaskDeleteAPIView.as_view(), name="task_delete"),
    # # REST API
    # path("", include(router.urls)),
]

# Class Based Views
# urlpatterns = [
#     path("", views.TaskListView.as_view(), name="task_list"),
#     path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
#     path("task/create/", views.TaskCreateView.as_view(), name="task_create"),
#     path("task/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
#     path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
#     path(
#         "task/<int:task_pk>/subtask/create/",
#         views.SubTaskCreateView.as_view(),
#         name="subtask_create",
#     ),
#     path("register/", views.UserRegisterView.as_view(), name="register"),
#     path("login/", views.UserLoginView.as_view(), name="login"),
#     path("logout/", views.UserLogoutView.as_view(), name="logout"),
# ]

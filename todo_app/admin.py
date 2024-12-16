from django.contrib import admin
from .models import Task, SubTask, Category,Team,TeamMembership

# Register your models here.
# admin.site.register(Task)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "due_date", "completed")


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "completed")


admin.site.register(Category)

admin.site.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name","members")

admin.site.register(TeamMembership)

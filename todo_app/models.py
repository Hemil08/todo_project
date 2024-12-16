from django.db import models
from django.contrib.auth.models import User

# DefaultUser = User()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    members = models.ManyToManyField(
        User,through="TeamMembership",related_name="teams"
    )

    def __str__(self):
        return self.name

# Team Membership Model
class TeamMembership(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "team"
        )
    
    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
    
# Invitation Model

class Invitation(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="invitations")
    invited_user = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="invitations_received"
    )
    sender = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="invitations_sent"
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"invitation for {self.invited_user.username} to join {self.team.name}"


# Create your models here.
class Task(models.Model):

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Low")
    due_date = models.DateField()

    # New field for many-to-many relationship with Category
    categories = models.ManyToManyField(Category, related_name="tasks", blank=True)

    # Team and assigned user
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="tasks",null=True,blank=True
    )
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} (Subtask of {self.task.title})"


class Comment(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task.title}"
    
    def is_reply(self):
        return self.parent is not None
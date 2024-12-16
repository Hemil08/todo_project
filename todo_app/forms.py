from django import forms
from .models import Task, Category, Comment, Team, User


class TaskForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # You can also use SelectMultiple if you prefer a dropdown
        required=False,
    )

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    assigned_user = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Initially set to none, populated dynamically based on team selection
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "completed",
            "priority",
            "due_date",
            "categories",
            "team",
            "assigned_user",
        ]

    def __init__(self, *args, **kwargs):
        # Get initial team to filter assigned users if necessary
        team_id = kwargs.pop("team_id", None)
        super().__init__(*args, **kwargs)

        # Populate assigned_user field based on team selection if available
        if team_id:
            team = Team.objects.get(id=team_id)
            self.fields["assigned_user"].queryset = team.members.all()
        elif self.instance and self.instance.team:
            # If editing a task with a team, populate assigned_user with team members
            self.fields["assigned_user"].queryset = self.instance.team.members.all()
        else:
            self.fields["assigned_user"].queryset = User.objects.none()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment..."}
            ),
        }

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name","description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class":"form-control","placeholder":"Enter Team Name"}
            ),
            "description" : forms.Textarea(
                attrs={
                    "class":"form-control",
                    "placeholder":"Enter team description",
                    "rows":3,
                }
            ),
        }
from django import forms
from .models import Task, Category, Comment


class TaskForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # You can also use SelectMultiple if you prefer a dropdown
        required=False,
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
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment..."}
            ),
        }

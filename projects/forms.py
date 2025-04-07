from django import forms
from .models import Project, ProjectImage, Comment, Rating


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fildes = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'tags']

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']


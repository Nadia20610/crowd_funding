from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Comment, Rating , ProjectImage , Report
from django.utils import timezone

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'tags', 'total_target', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time < timezone.now():
                raise ValidationError("Start time cannot be in the past")
            if end_time <= start_time:
                raise ValidationError("End time must be after start time")
        
        return cleaned_data

class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'is_featured']

class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

class ProjectReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
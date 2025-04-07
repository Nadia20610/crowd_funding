from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    title = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    total_target = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    @property
    def days_left(self):
        return (self.end_time - timezone.now()).days if self.end_time > timezone.now() else 0
    
    @property
    def total_donations(self):
        return self.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    @property
    def progress(self):
        return min(100, (self.total_donations / self.total_target) * 100)
    
    def can_be_cancelled(self):
        return self.progress < 25 and not self.is_cancelled
    
    def __str__(self):
        return self.title

class ProjectPicture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='projects/')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.project.title}"

class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Comment by {self.user.email} on {self.project.title}"

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('project', 'user')
    
    def __str__(self):
        return f"{self.rating} stars by {self.user.email} for {self.project.title}"

class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('project', 'user')
    
    def __str__(self):
        return f"Report on {self.project.title} by {self.user.email}"
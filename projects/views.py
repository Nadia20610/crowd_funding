from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Avg, Q
from .models import Project, ProjectComment, ProjectRating, ProjectReport, ProjectPicture, Category
from .forms import ProjectForm, ProjectCommentForm, ProjectRatingForm, ProjectReportForm, ProjectPictureForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_cancelled=False,
            end_time__gt= timezone.now()
        ).annotate(
            avg_rating=Avg('ratings__rating')
        )
        
        if 'category' in self.kwargs:
            queryset = queryset.filter(category__slug=self.kwargs['category'])
        
        if 'search' in self.request.GET:
            search_term = self.request.GET['search']
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(tags__name__icontains=search_term)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Add comment form
        context['comment_form'] = ProjectCommentForm()
        
        # Add rating form (if user hasn't rated yet)
        if self.request.user.is_authenticated:
            user_rating = ProjectRating.objects.filter(
                project=project,
                user=self.request.user
            ).first()
            if not user_rating:
                context['rating_form'] = ProjectRatingForm()
            else:
                context['user_rating'] = user_rating
        
        # Calculate average rating
        context['average_rating'] = project.ratings.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        
        # Get similar projects (by tags)
        similar_projects = Project.objects.filter(
            tags__in=project.tags.all()
        ).exclude(
            id=project.id
        ).distinct()[:4]
        context['similar_projects'] = similar_projects
        
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple pictures upload
        pictures = self.request.FILES.getlist('pictures')
        for i, picture in enumerate(pictures):
            ProjectPicture.objects.create(
                project=self.object,
                image=picture,
                is_featured=(i == 0)  # First image is featured by default
            )
        
        messages.success(self.request, "Project created successfully!")
        return response
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.pk})

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator != request.user:
            messages.error(request, "You can't edit this project")
            return redirect('project-detail', pk=project.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.pk})

class ProjectCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        
        if project.creator != request.user:
            messages.error(request, "You can't cancel this project")
            return redirect('project-detail', pk=project.pk)
        
        if not project.can_be_cancelled():
            messages.error(request, "Project can't be cancelled as it has reached 25% of target")
            return redirect('project-detail', pk=project.pk)
        
        project.is_cancelled = True
        project.save()
        messages.success(request, "Project cancelled successfully")
        return redirect('project-detail', pk=project.pk)

# Add similar views for comments, ratings, reports following the same pattern
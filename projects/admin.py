from django.contrib import admin
from .models import (
    Category, Tag, Project, 
    ProjectPicture, ProjectComment,
    ProjectRating, ProjectReport
)

class ProjectPictureInline(admin.TabularInline):
    model = ProjectPicture
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'total_target', 'start_time', 'end_time', 'is_featured')
    list_filter = ('category', 'is_featured', 'is_cancelled')
    search_fields = ('title', 'details')
    inlines = [ProjectPictureInline]

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectComment)
admin.site.register(ProjectRating)
admin.site.register(ProjectReport)
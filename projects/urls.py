from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView,
    ProjectCreateView, ProjectUpdateView,
    ProjectCancelView
    # , 
    # add_comment,
    # add_rating, report_project
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('category/<slug:category>/', ProjectListView.as_view(), name='project-list-by-category'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/cancel/', ProjectCancelView.as_view(), name='project-cancel'),
    # path('<int:pk>/comment/', add_comment, name='add-comment'),
    # path('<int:pk>/rate/', add_rating, name='add-rating'),
    # path('<int:pk>/report/', report_project, name='report-project'),
]
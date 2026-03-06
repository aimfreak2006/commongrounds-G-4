from django.urls import path
from .views import ProjectCategoryListView, ProjectDetailView

urlpatterns = [
    path(
     'projects/',
     ProjectCategoryListView.as_view(),
     name='all-projects'
     ),
    path(
     'project/<int:pk>',
     ProjectDetailView.as_view(),
     name='project-details'
     ),
]

app_name = "diyprojects"

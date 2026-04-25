from django.urls import path
from .views import (ProjectCategoryListView, 
                    ProjectDetailView,
                    ProjectCreateView,
                    ProjectUpdateView)

urlpatterns = [
    path(
      'projects/',
      ProjectCategoryListView.as_view(),
      name='all-projects'),
    path(
      'project/<int:pk>',
      ProjectDetailView.as_view(),
      name='project-details'),
    path(
      'project/add',
      ProjectCreateView.as_view(), 
      name='project-add'),
    path(
      'project/<int:pk>/edit',
      ProjectUpdateView.as_view(),
      name='project-update'),
]

app_name = "diyprojects"

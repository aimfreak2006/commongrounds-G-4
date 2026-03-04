from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('projects/',
         ProjectCategoryListView.as_view(),
         name='all-projects'
         ),
    path('project/<int:pk>',
         ProjectDetailView.as_view(),
         name='project-details'),
]

app_name = "diyprojects"

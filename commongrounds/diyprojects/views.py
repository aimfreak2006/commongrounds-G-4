from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *


class ProjectCategoryListView(ListView):
    model = ProjectCategory
    template_name = "diyprojects/project_list.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "diyprojects/project_detail.html"

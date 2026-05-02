from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import (Project, ProjectReview, 
                     ProjectRating, ProjectCategory, 
                     Favorite)
from django.db.models import Avg
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        UserPassesTestMixin)
from django.views.generic.edit import CreateView, UpdateView
from .forms import ProjectReviewForm, ProjectRatingForm
from django.shortcuts import redirect


class ProjectCategoryListView(ListView):
    model = Project
    template_name = "diyprojects/project_list.html"
    context_object_name = 'all_projects'

    def get_context_data(self, **kwargs):
            
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['categories'] = ProjectCategory.objects.all()
        
        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            context['created_projects'] = Project.objects.filter(creator=profile)
            context['favorited_projects'] = Project.objects.filter(favorites__profile=profile)
            context['reviewed_projects'] = Project.objects.filter(reviews__reviewer=profile)
        
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "diyprojects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        user = self.request.user

        raw_avg = project.ratings.aggregate(Avg('score'))['score__avg']
        context['avg_rating'] = round(raw_avg, 2) if raw_avg else 0
        context['total_favorites'] = project.favorites.count()
        context['rating_form'] = ProjectRatingForm()
        context['review_form'] = ProjectReviewForm()
        context['reviews'] = self.object.reviews.all()

        is_favorited = False
        if user.is_authenticated and hasattr(user, 'profile'):
            is_favorited = project.favorites.filter(profile=user.profile).exists()
        context['is_favorited'] = is_favorited
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_profile = request.user.profile

        if 'submit_rating' in request.POST:
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                ProjectRating.objects.update_or_create(
                    profile=request.user.profile,
                    project=self.object,
                    defaults={
                        'score': form.cleaned_data['score']
                    }
                )
                
        elif 'submit_review' in request.POST:

            form = ProjectReviewForm(request.POST, request.FILES)
            if form.is_valid():
                ProjectReview.objects.update_or_create(
                    reviewer=request.user.profile,
                    project=self.object,
                    defaults={
                        'comment': form.cleaned_data['comment'],
                        'image': form.cleaned_data.get('image')
                    }
                )

        elif 'submit_favorite' in request.POST:
            from .models import Favorite # Import here or at top
            favorite_qs = Favorite.objects.filter(
                project=self.object, 
                profile=request.user.profile
            )
            
            if favorite_qs.exists():
                favorite_qs.delete()
            else:
                Favorite.objects.create(
                    project=self.object, 
                    profile=request.user.profile
                )
        return redirect('diyprojects:project-details', pk=self.object.pk)


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = "diyprojects/project_create.html"

    def test_func(self):
        return self.request.user.profile.role == "Project Creator"

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = "diyprojects/project_update.html"

    def test_func(self):
        profile = self.request.user.profile
        return profile.role == "Project Creator" and self.get_object().creator == profile


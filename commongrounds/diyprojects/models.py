from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile
from  django.core.validators import MinValueValidator, MaxValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diyprojects:category-details', args=[str(self.pk)])

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']
        verbose_name = 'project category'
        verbose_name_plural = 'project categories'


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='projects'
                                )
    creator = models.ForeignKey(Profile,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='projects'
                                )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} last updated on {}'.format(self.title, self.updated_on)

    def get_absolute_url(self):
        return reverse('diyprojects:project-details', args=[str(self.pk)])

    @property
    def is_valid(self):
        return self.created_on > self.updated_on

    class Meta:
        ordering = ['-created_on']
        unique_together = ['title', 'created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'


class Favorite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='favorites')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    date_favorited = models.DateField(auto_now_add=True)
    status_choices = models.TextChoices('Status', 'Backlog To-Do Done')
    project_status = models.CharField(max_length=20, choices=status_choices.choices, default=status_choices.Backlog)

    class Meta:
        unique_together = ['profile', 'project']
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'

    def __str__(self):
        return f"{self.profile.display_name} favorited {self.project.title}"


class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    image = models.ImageField(upload_to='project_reviews_imgs', null=True, blank=True)

    class Meta:
        unique_together = ['reviewer', 'project']
        verbose_name = 'project review'
        verbose_name_plural = 'project reviews'

    def __str__(self):
        return f"{self.reviewer.display_name} reviewed {self.project.title}"


class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return f"{self.profile.display_name} rated {self.project.title} {self.score} stars"
 
    class Meta:
        unique_together = ['profile', 'project']
        verbose_name = 'project rating'
        verbose_name_plural = 'project ratings'

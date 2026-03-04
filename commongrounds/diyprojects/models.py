from django.db import models
from django.urls import reverse


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diyprojects:all-projects', args=[str(self.pk)])

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']
        verbose_name = 'project category'
        verbose_name_plural = 'project categories'


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory,
                                 on_delete=models.CASCADE,
                                 related_name='projects'
                                 )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    def __str__(self):
        return '{} last updated on {}'.format(self.title, self.updated_on)

    def get_absolute_url(self):
        return reverse('diyprojects:project-details', args=[str(self.pk)])

    @property
    def is_valid(self):
        return self.created_on > self.updated_on

    class Meta:
        ordering = ['created_on']
        unique_together = ['title', 'created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'

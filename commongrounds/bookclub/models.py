from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        unique_together = ['name', 'description',]
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='books'
    )
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    def __str__(self):
        return '{} last updated on {}'.format(self.title, self.updated_on)

    def get_absolute_url(self):
        return reverse('bookclub:book_details', args=[str(self.pk)])

    @property
    def is_valid(self):
        return self.created_on > self.updated_on

    class Meta:
        ordering = ['-publication_year',]
        unique_together = ['title', 'created_on',]
        verbose_name = 'book'
        verbose_name_plural = 'books'

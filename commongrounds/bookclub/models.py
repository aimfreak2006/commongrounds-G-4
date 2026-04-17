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
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
    )
    contributor = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.SET_NULL,
        related_name='contributed_books',
        null=True
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField()
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} last updated on {}'.format(self.title, self.updated_on)

    def get_absolute_url(self):
        return reverse('bookclub:book_details', args=[str(self.pk)])

    class Meta:
        ordering = ['-publication_year',]
        unique_together = ['title', 'created_on',]
        verbose_name = 'book'
        verbose_name_plural = 'books'


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    anon_reviewer = models.CharField(max_length=255, blank=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        reviewer_name = self.user_reviewer or self.anon_reviewer or 'Anonymous'
        return '{} on {}'.format(reviewer, self.book.title)


class Bookmark(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} bookmarked {}'.format(self.profile, self.book.title)


class Borrow(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrows'
    )
    borrower = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='borrows',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, blank=True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        borrower_name = self.borrower or self.name or 'Anonymous'
        return '{} borrowed {}'.format(borrower_name, self.book.title)

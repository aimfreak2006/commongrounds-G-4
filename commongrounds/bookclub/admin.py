from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow


class BookInLine(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    search_fields = ('name',)
    list_display = ('name', 'description',)
    inlines = [BookInLine,]


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'author',)
    readonly_fields = ('created_on', 'updated_on',)
    list_display = (
        'title', 'genre', 'contributor', 'author',
        'publication_year', 'available_to_borrow',
        'created_on', 'updated_on',
    )
    list_filter = (
        'genre', 'available_to_borrow',
        'publication_year', 'created_on',
    )
    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'author', 'publication_year'),
                'genre',
                'contributor',
                'synopsis',
                'available_to_borrow',
                ('created_on', 'updated_on'),
            ]
        }),
    ]


class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview
    search_fields = ('title', 'comment',)
    list_display = ('title', 'book', 'user_reviewer', 'anon_reviewer',)
    list_filter = ('book',)


class BookmarkAdmin(admin.ModelAdmin):
    model = Bookmark
    list_display = ('profile', 'book', 'date_bookmarked',)
    list_filter = ('book', 'date_bookmarked',)


class BorrowAdmin(admin.ModelAdmin):
    model = Borrow
    list_display = ('book', 'borrower', 'name', 'date_borrowed', 'date_to_return',)
    list_filter = ('book', 'date_borrowed',)
    readonly_fields = ('date_to_return',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Borrow, BorrowAdmin)
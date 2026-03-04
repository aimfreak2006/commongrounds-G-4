from django.contrib import admin
from .models import Book, Genre


class BookInLine(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    search_fields = ('name',)
    list_display = ('name', 'description',)
    inline = [BookInLine,]


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'author',)
    list_display = (
        'title', 'genre', 'author', 'publication_year',
        'created_on', 'updated_on',
    )
    list_filter = (
        'genre', 'publication_year',
        'created_on', 'updated_on',
    )
    fieldsets = [
        ('Details', {
            'fields': [
                (
                    'title', 'author', 'publication_year',
                    'created_on', 'updated_on',
                ),
                'genre',
            ]
        }),
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)

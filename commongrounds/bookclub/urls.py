from django.contrib import admin
from django.urls import path, include
from .views import BookListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book_details'),
]

app_name = "bookclub"
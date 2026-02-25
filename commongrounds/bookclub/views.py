from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from .models import 

class BookListView(ListView):
    model = Genre
    template_name = "bookclub/book_list.html"

class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/book_details.html"
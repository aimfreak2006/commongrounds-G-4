from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Book, Bookmark, Borrow
from .forms import BookBorrowForm, BookFormFactory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from datetime import timedelta, date
from accounts.mixins import RoleRequiredMixin


class BookListView(ListView):
    model = Book
    template_name = "bookclub/book_list.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books = Book.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            contributed = Book.objects.filter(contributor=profile)
            bookmarked = Book.objects.filter(bookmarks__profile=profile)
            reviewed = Book.objects.filter(reviews__user_reviewer=profile)

            grouped_pks = (
                contributed.values('pk') |
                bookmarked.values('pk') |
                reviewed.values('pk')
            )

            context['contributed_books'] = contributed
            context['bookmarked_books'] = bookmarked
            context['reviewed_books'] = reviewed
            context['all_books'] = all_books.exclude(pk__in=grouped_pks)
        else:
            context['all_books'] = all_books

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/book_details.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        context['review_form'] = (
            BookFormFactory.get_form('review', self.request)
        )
        context['reviews'] = book.reviews.all()
        context['bookmark_count'] = book.bookmarks.count()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_bookmarked'] = (
                book.bookmarks.filter(profile=profile).exists()
            )
            context['is_contributor'] = book.contributor == profile

        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if 'bookmark' in request.POST:
            if request.user.is_authenticated:
                profile = request.user.profile
                bookmark = Bookmark.objects.filter(profile=profile, book=book)
                if bookmark.exists():
                    bookmark.delete()
                else:
                    Bookmark.objects.create(profile=profile, book=book)
            return redirect('bookclub:book_details', pk=book.pk)

        form = BookFormFactory.get_form('review', request)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if request.user.is_authenticated:
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = 'Anonymous'
            review.save()
            return redirect('bookclub:book_details', pk=book.pk)

        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)


class BookCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Book
    template_name = "bookclub/book_create.html"
    allowed_roles = ['Book Contributor']

    def get_form(self, form_class=None):
        return BookFormFactory.get_form('contribute', self.request)

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BookUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Book
    template_name = "bookclub/book_update.html"
    allowed_roles = ['Book Contributor']

    def get_form(self, form_class=None):
        return BookFormFactory.get_form(
            'update', self.request, instance=self.object
        )

    def get_queryset(self):
        return Book.objects.filter(contributor=self.request.user.profile)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BookBorrowView(CreateView):
    model = Borrow
    form_class = BookBorrowForm
    template_name = "bookclub/book_borrow.html"

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):  # double check if name should still editable if logged in
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            name_field = form.fields['name']
            name_field.required = False
            name_field.initial = self.request.user.profile.display_name
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

    def form_valid(self, form):  # double check if available_to_borrow should be changed
        borrow = form.save(commit=False)
        borrow.date_borrowed = (
            form.cleaned_data['date_borrowed'] or date.today()
        )

        if borrow.date_borrowed < date.today():
            form.add_error(
                'date_borrowed', 'Borrow date cannot be in the past.'
            )
            return self.form_invalid(form)

        borrow.book = self.book
        borrow.date_to_return = borrow.date_borrowed + timedelta(weeks=2)
        if self.request.user.is_authenticated:
            borrow.borrower = self.request.user.profile
            if not borrow.name:
                borrow.name = self.request.user.profile.display_name
        borrow.save()
        return redirect('bookclub:book_details', pk=self.book.pk)

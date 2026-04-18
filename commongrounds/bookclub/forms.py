from django import forms
from .models import BookReview, Book, Borrow
from datetime import date


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment',]


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow',]


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow',]


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']
        widgets = {
            'date_borrowed': forms.DateInput(attrs={
                'type': 'date',
                'min': date.today().isoformat(),
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_borrowed'].required = False
from django import forms
from .models import Book,Reviews,Purchase

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['area',]
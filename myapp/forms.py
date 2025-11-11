from django import forms
from .models import Order, Review, Book

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [('B', 'Borrow'), ('P', 'Purchase')]
    # Multiple selections + checkboxes:
    feedback = forms.MultipleChoiceField(
        choices=FEEDBACK_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='Your Name')

    category = forms.ChoiceField(
        required=False,
        label='Select a category:',
        choices=[('', '--- Any ---')] + list(Book.CATEGORY_CHOICES),
        widget=forms.RadioSelect
    )

    max_price = forms.IntegerField(
        label='Maximum Price',
        min_value=0,
        required=True
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect,
        }
        labels = {'member': 'Member name'}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {
            'book': forms.RadioSelect
        }
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)',
        }
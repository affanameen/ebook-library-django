from django import forms
from .models import Book

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [('B', 'Borrow'), ('P', 'Purchase')]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

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

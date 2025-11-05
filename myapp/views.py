from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm
from .models import Book

def index(request):
    booklist = Book.objects.all().order_by('id')
    return render(request, 'myapp/index.html', {'booklist': booklist})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail.html', {'book': book})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else:
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})
def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category'] or ''  # may be empty
            max_price = form.cleaned_data['max_price']

            qs = Book.objects.filter(price__lte=max_price)
            if category:
                qs = qs.filter(category=category)

            booklist = qs.order_by('id')

            return render(request, 'myapp/results.html', {
                'name': name,
                'category': category,
                'booklist': booklist,
            })
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})

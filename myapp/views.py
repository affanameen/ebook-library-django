from django.shortcuts import render, get_object_or_404
from .models import Book

def index(request):
    booklist = Book.objects.all().order_by('id')
    return render(request, 'myapp/index.html', {'booklist': booklist})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail.html', {'book': book})

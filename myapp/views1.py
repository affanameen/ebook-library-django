from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Publisher, Book

def index(request):
    response = HttpResponse()

    # Books ordered by primary key
    response.write('<p><strong>Books:</strong></p>')
    books_by_pk = Book.objects.all().order_by('id')
    for b in books_by_pk:
        if b.price == 0:
            price_display = "Free Book"
        else:
            price_display = f"${b.price:.2f}"
        response.write(f'<p>{b.id}: {b.title} — {price_display}</p>')

    # Publishers sorted by city in desc
    response.write('<hr>')
    response.write('<p><strong>Publishers:</strong></p>')
    pubs = Publisher.objects.all().order_by('-city')  # DESC by city
    for p in pubs:
        response.write(f'<p>{p.name} — {p.city}</p>')

    return response

def about(request):
    return HttpResponse("This is an eBook APP.")

def detail(request, book_id: int):
    """
    Show title (uppercase), price with $, and publisher for the given book_id.
    Return 404 if not found.
    """
    book = get_object_or_404(Book, pk=book_id)
    title_upper = book.title.upper()
    price_fmt = f"${book.price:.2f}"
    publisher_name = book.publisher.name if book.publisher_id else "—"

    html = f"""
        <h1>{title_upper}</h1>
        <p><strong>Price:</strong> {price_fmt}</p>
        <p><strong>Publisher:</strong> {publisher_name}</p>
    """
    return HttpResponse(html)

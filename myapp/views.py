from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from .models import Book, Review

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
            selected = form.cleaned_data['feedback']  # list like ['B','P'] or ['B']
            # Build a friendly sentence
            mapping = {'B': 'borrow', 'P': 'purchase'}
            human = [mapping.get(x, x) for x in selected]
            # e.g., "to borrow and purchase books." / "to borrow books."
            if not human:
                msg = "No preference selected."
            elif len(human) == 1:
                msg = f"to {human[0]} books."
            else:
                msg = f"to {' and '.join(human)} books."
            return render(request, 'myapp/fb_results.html', {'choice': ' ' + msg})
        else:
            return render(request, 'myapp/feedback.html', {'form': form})
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

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the Order without M2M first
            order = form.save(commit=False)
            member = order.member
            order_type = order.order_type
            order.save()

            # Now save many-to-many (books)
            form.save_m2m()  # Ensures selected books are attached to 'order'

            # If type == 1 (borrow), add each ordered book to member.borrowed_books
            if order_type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)

            # Pass both books and order to the response template
            books = order.books.all()
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                # Save the review
                rv = form.save()

                # Increment the book's num_reviews
                book = rv.book
                book.num_reviews = (book.num_reviews or 0) + 1
                book.save(update_fields=['num_reviews'])

                # Redirect to main page
                return redirect('myapp:index')
            else:
                # Not in range: redisplay with message
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
                return render(request, 'myapp/review.html', {'form': form})
        else:
            # Form invalid -> default errors shown by {{ form.as_p }}
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})

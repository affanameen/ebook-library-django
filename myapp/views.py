from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from .models import Book, Review, Member
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg
import random

def index(request):
    booklist = Book.objects.all().order_by('id')

    last_login = request.session.get('last_login', None)
    if last_login:
        last_login_msg = f"Your last login was at: {last_login}"
    else:
        last_login_msg = "Your last login was more than one hour ago."

    return render(request, 'myapp/index.html', {
        'booklist': booklist,
        'last_login_msg': last_login_msg,
    })


def about(request):
    # --- Lucky number cookie logic ---
    lucky_cookie = request.COOKIES.get('lucky_num')

    if lucky_cookie:
        mynum = int(lucky_cookie)
    else:
        mynum = random.randint(1, 100)

    response = render(request, 'myapp/about.html', {'mynum': mynum})

    # Set cookie to expire in 5 minutes (300 seconds)
    response.set_cookie('lucky_num', mynum, max_age=300)

    return response


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

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                # --- Lab 9: save last_login in session and set expiry ---
                now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                request.session['last_login'] = now
                request.session.set_expiry(3600)  # 1 hour

                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def chk_reviews(request, book_id):
    # Correct way: Member IS the user, so use pk or username
    try:
        member = Member.objects.get(pk=request.user.pk)
        # or: Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        message = 'You are not a registered member!'
        return render(request, 'myapp/chk_reviews.html', {
            'message': message,
            'book': None,
            'avg_rating': None,
        })

    # User is a Member → proceed to book and reviews
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book)

    if reviews.exists():
        agg = reviews.aggregate(avg=Avg('rating'))
        avg_rating = round(agg['avg'], 2)
        message = None
    else:
        avg_rating = None
        message = 'There are no reviews submitted for this book yet.'

    return render(request, 'myapp/chk_reviews.html', {
        'book': book,
        'avg_rating': avg_rating,
        'message': message,
    })


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Canada')

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Science & Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
    ]
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()} (${self.price})"


class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField('Book', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow'),
    ]
    books = models.ManyToManyField(Book, blank=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def total_items(self):
        return self.books.count()

    def __str__(self):
        return f"Order #{self.pk} - {self.member} - {self.get_order_type_display()} on {self.order_date}"

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)  # optional
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.reviewer} — {self.book.title} ({self.rating}/5)"

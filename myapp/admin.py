from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# ------------------ Publisher ------------------
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'city', 'country')
    list_display_links = ('name',)
    search_fields = ('name', 'city', 'country')


# ------------------ Book ------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # edit-page layout (Lab 10)
    fields = [
        ('title', 'category', 'publisher'),
        ('pages', 'price', 'num_reviews'),
        'description',
    ]
    list_display = ('title', 'category', 'price')
    list_filter = ('category', 'publisher')
    search_fields = ('title',)



# ------------------ Member ------------------
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'status',
        'address', 'city', 'province', 'auto_renew',
        'last_renewal', 'borrowed_books_ids', 'borrow_count'
    )
    list_display_links = ('first_name', 'last_name')
    list_filter = ('status', 'auto_renew', 'province', 'city')
    search_fields = ('first_name', 'last_name', 'username', 'city')

    def borrow_count(self, obj):
        """Number of books this member has borrowed."""
        return obj.borrowed_books.count()
    borrow_count.short_description = 'Borrowed Count'

    def borrowed_books_ids(self, obj):
        return ", ".join(str(book.id) for book in obj.borrowed_books.all()) or "-"
    borrowed_books_ids.short_description = 'Borrowed Book IDs'


# ------------------ Order ------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # edit-page layout (Lab 10)
    fields = [
        ('books',),
        ('member', 'order_type', 'order_date'),
    ]

    # list page columns (Lab 10)
    list_display = (
        'id', 'member', 'order_type', 'order_date', 'total_items'
    )

    # optional: keep filters/search
    list_filter = ('order_type', 'order_date')
    search_fields = ('member__username', 'books__title')

    def books_ids(self, obj):
        return ", ".join(str(book.id) for book in obj.books.all())
    books_ids.short_description = 'Book IDs'

# ------------------ Review ------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'book', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('reviewer', 'book__title')
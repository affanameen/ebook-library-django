from django.contrib import admin
from .models import Publisher, Book, Member, Order


# ------------------ Publisher ------------------
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'city', 'country')
    list_display_links = ('name',)
    search_fields = ('name', 'city', 'country')


# ------------------ Book ------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'pages', 'price', 'publisher')
    list_display_links = ('title',)
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
        """Show comma-separated list of borrowed book IDs."""
        return ", ".join(str(book.id) for book in obj.borrowed_books.all()) or "-"
    borrowed_books_ids.short_description = 'Borrowed Book IDs'


# ------------------ Order ------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'member', 'order_type', 'order_date',
        'books_ids', 'total_items'
    )
    list_filter = ('order_type', 'order_date')
    search_fields = ('member__username', 'books__title')

    def books_ids(self, obj):
        return ", ".join(str(book.id) for book in obj.books.all())
    books_ids.short_description = 'Book IDs'

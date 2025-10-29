import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysiteF25.settings')
django.setup()

from myapp.models import Publisher, Book, Member, Order
from django.contrib.auth.models import User
from django.utils import timezone

# --- Publishers --------------------------------------------------------------
publishers_data = [
    {'name': 'Wiley', 'website': 'https://www.wiley.com/', 'city': 'Hoboken', 'country': 'USA'},
    {'name': 'Pearson', 'website': 'https://www.pearson.com/', 'city': 'London', 'country': 'UK'},
    {'name': 'Penguin Random House', 'website': 'https://www.penguinrandomhouse.com/', 'city': 'New York', 'country': 'USA'},
]

publisher_objs = {}
for data in publishers_data:
    pub, _ = Publisher.objects.get_or_create(name=data['name'], defaults=data)
    publisher_objs[data['name']] = pub

# --- Books -------------------------------------------------------------------
books_data = [
    {'title': 'Machine Learning For Dummies', 'category': 'S', 'pages': 464, 'price': 34.99, 'publisher': 'Wiley'},
    {'title': 'Data Science For Dummies', 'category': 'S', 'pages': 432, 'price': 36.99, 'publisher': 'Wiley'},
    {'title': 'Artificial Intelligence', 'category': 'S', 'pages': 1136, 'price': 197.32, 'publisher': 'Pearson'},
    {'title': 'Computer Networking', 'category': 'S', 'pages': 720, 'price': 143.99, 'publisher': 'Pearson'},
    {'title': 'The Night Circus', 'category': 'F', 'pages': 400, 'price': 41.00, 'publisher': 'Penguin Random House'},
    {'title': 'The Underground Railroad', 'category': 'F', 'pages': 320, 'price': 26.95, 'publisher': 'Penguin Random House'},
    {'title': 'Becoming', 'category': 'B', 'pages': 464, 'price': 45.00, 'publisher': 'Penguin Random House'},
    {'title': 'A Walk in the Woods', 'category': 'T', 'pages': 304, 'price': 19.00, 'publisher': 'Penguin Random House'},
]

book_objs = {}
for b in books_data:
    book, _ = Book.objects.get_or_create(
        title=b['title'],
        defaults={
            'category': b['category'],
            'pages': b['pages'],
            'price': b['price'],
            'publisher': publisher_objs[b['publisher']],
        }
    )
    book_objs[b['title']] = book

# --- Members -----------------------------------------------------------------
members_data = [
    {'username': 'elena', 'first_name': 'Elena', 'last_name': 'Kwon', 'status': 2,
     'address': '102 Elm Avenue', 'city': 'Vancouver', 'province': 'BC',
     'last_renewal': '2024-04-30', 'auto_renew': True,
     'password': 'Elena@102', 'borrowed_books': ['Machine Learning For Dummies', 'The Night Circus']},
    {'username': 'marcus', 'first_name': 'Marcus', 'last_name': 'Reed', 'status': 1,
     'address': '88 Forest Hill Dr', 'city': 'Ottawa', 'province': 'ON',
     'last_renewal': '2024-03-20', 'auto_renew': True,
     'password': 'Marcus!88', 'borrowed_books': ['Artificial Intelligence', 'The Night Circus']},
    {'username': 'priya', 'first_name': 'Priya', 'last_name': 'Shah', 'status': 1,
     'address': '21 Lakeview Terrace', 'city': 'Saskatoon', 'province': 'SK',
     'last_renewal': '2024-02-15', 'auto_renew': False,
     'password': 'Priya#21', 'borrowed_books': []},
    {'username': 'james', 'first_name': 'James', 'last_name': 'Bennett', 'status': 3,
     'address': '65 Cedar Avenue', 'city': 'Ottawa', 'province': 'ON',
     'last_renewal': '2024-04-10', 'auto_renew': True,
     'password': 'James2024', 'borrowed_books': ['Data Science For Dummies', 'The Night Circus']},
    {'username': 'aisha', 'first_name': 'Aisha', 'last_name': 'Ncube', 'status': 2,
     'address': '400 Heritage Blvd', 'city': 'Winnipeg', 'province': 'MB',
     'last_renewal': '2024-05-12', 'auto_renew': True,
     'password': 'Aisha!400', 'borrowed_books': ['The Underground Railroad', 'Becoming', 'A Walk in the Woods']},
    {'username': 'leo', 'first_name': 'Leo', 'last_name': 'Kwon', 'status': 2,
     'address': '77 Riverstone Crescent', 'city': 'Ottawa', 'province': 'ON',
     'last_renewal': '2024-03-05', 'auto_renew': False,
     'password': 'Leo@River', 'borrowed_books': []},
]

member_objs = {}
for m in members_data:
    borrowed = m.pop('borrowed_books')
    raw_pw = m.pop('password')
    member, created = Member.objects.get_or_create(username=m['username'], defaults=m)
    member.set_password(raw_pw)
    member.save()
    for title in borrowed:
        member.borrowed_books.add(book_objs[title])
    member_objs[m['username']] = member

# --- Orders ------------------------------------------------------------------
orders_data = [
    {'member': 'elena', 'books': ['Machine Learning For Dummies', 'The Night Circus'], 'order_type': 1, 'order_date': '2024-04-02'},
    {'member': 'marcus', 'books': ['Artificial Intelligence', 'The Night Circus'], 'order_type': 1, 'order_date': '2024-03-19'},
    {'member': 'aisha', 'books': ['The Underground Railroad', 'Becoming', 'A Walk in the Woods'], 'order_type': 1, 'order_date': '2024-04-05'},
    {'member': 'james', 'books': ['Data Science For Dummies', 'The Night Circus'], 'order_type': 1, 'order_date': '2024-03-29'},
    {'member': 'leo', 'books': ['The Night Circus', 'A Walk in the Woods'], 'order_type': 0, 'order_date': '2024-03-01'},
    {'member': 'elena', 'books': ['Artificial Intelligence'], 'order_type': 0, 'order_date': '2024-04-01'},
    {'member': 'aisha', 'books': ['Computer Networking'], 'order_type': 0, 'order_date': '2024-04-06'},
]

for o in orders_data:
    order = Order.objects.create(
        member=member_objs[o['member']],
        order_type=o['order_type'],
        order_date=o['order_date']
    )
    for title in o['books']:
        order.books.add(book_objs[title])

# --- Superuser ---------------------------------------------------------------
admin_user = "affan"
admin_pass = "affan123"
if not User.objects.filter(username=admin_user).exists():
    User.objects.create_superuser(admin_user, "admin@example.com", admin_pass)
    print(f"👑 Superuser created: {admin_user} / {admin_pass}")
else:
    print("👑 Superuser already exists.")

print("\n✅ Database populated successfully!\n")
print(f"Publishers: {Publisher.objects.count()}")
print(f"Books:      {Book.objects.count()}")
print(f"Members:    {Member.objects.count()}")
print(f"Orders:     {Order.objects.count()}")

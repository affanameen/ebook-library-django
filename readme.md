# 📚 Django eBook App

This Django-based web application demonstrates Django fundamentals including **models, views, templates, URL routing, template inheritance, and static file handling**.

---

## 🚀 Features

- 📘 **Dynamic Book Listing**
  - Displays all books stored in the database.
  - Shows “Free Book” label when price = 0.

- 🧑‍💼 **Publisher Management**
  - Each book is linked to a publisher.
  - Information added via Django Admin interface.

- 🌐 **Multi-Page Navigation**
  - `/myapp/` → Book list  
  - `/myapp/about/` → About page  
  - `/myapp/<id>/` → Book details (title, price, publisher)

- 🎨 **Template Inheritance + CSS**
  - `base.html` provides common layout.
  - `index.html`, `about.html`, `detail.html` extend base.
  - Styled with `style.css` from Django static files.

---

## 🏗️ Project Structure
mysiteF25/
│
├── myapp/
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── admin.py
│ ├── static/
│ │ └── myapp/style.css
│ └── templates/
│ └── myapp/
│ ├── base.html
│ ├── index.html
│ ├── about.html
│ └── detail.html
│
└── mysiteF25/
├── settings.py
└── urls.py


---

💡 Key Concepts Demonstrated

Django MVC (MTV) pattern

Model creation, migrations, and admin interface

Dynamic HTML rendering with Django Template Language (DTL)

Template inheritance and reusable components

Static file management

Conditional rendering ({% if book.price == 0 %} → “Free Book”)

# myapp/urls.py
from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),              # /myapp/
    path('about/', views.about, name='about'),        # /myapp/about/
    path('<int:book_id>/', views.detail, name='detail'),  # /myapp/1/
]

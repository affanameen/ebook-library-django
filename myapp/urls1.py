# myapp/urls1.py
from django.urls import path
from myapp import views1

app_name = 'myapp'   # important for {% url 'myapp:index' %} to work

urlpatterns = [
    path('', views1.index, name='index'),           # /myapp/
    path('about/', views1.about, name='about'),     # /myapp/about/
    path('<int:book_id>/', views1.detail, name='detail'),  # /myapp/1/
]

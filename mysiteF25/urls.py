from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # OLD (Lab 5):
    # path('myapp/', include('myapp.urls1')),

    # NEW (Lab 6):
    path('myapp/', include('myapp.urls')),
]

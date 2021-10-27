from django.contrib import admin
from django.urls import path,include

urlpatterns = [
     path('doctors/',include('doctors.urls')),
     path('drugs/',include('drugs.urls')),
     path('admin/', admin.site.urls),
]


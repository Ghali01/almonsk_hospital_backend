from django.contrib import admin
from django.urls import path,include

urlpatterns = [
     path('doctors/',include('doctors.urls')),
     path('drugs/',include('drugs.urls')),
     path('surgeries/',include('surgeries.urls')),
     path('patients/',include('patients.urls')),
     path('admin/', admin.site.urls),
]


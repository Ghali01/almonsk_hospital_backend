from django.urls import path
from .views import  Doctors
urlpatterns=[ 
    path('',Doctors.as_view(),name='doctors'),
    path('<int:pk>',Doctors.as_view(),name='doctors')
]
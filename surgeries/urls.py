from django.urls import path
from .views import Surgeries
urlpatterns=[ 
    path('',Surgeries.as_view(),name='surgeries')
]
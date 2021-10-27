from django.urls import path
from .views import Drugs
urlpatterns=[ 
    path('',Drugs.as_view(),name='drugs'),
]
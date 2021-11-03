from django.urls import path
from .views import Drugs
urlpatterns=[ 
    path('<int:page>',Drugs.as_view(),name='drugs'),
    path('',Drugs.as_view(),name='drugs'),
]
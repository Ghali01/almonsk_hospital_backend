from django.urls import path
from .views import Surgeries
urlpatterns=[ 
    path('<int:page>',Surgeries.as_view(),name='surgeries'),
    path('',Surgeries.as_view(),name='surgeries')
]
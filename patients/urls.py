from django.urls import path
from patients.views import PatientCosts, Patients
urlpatterns=[ 
    path('costs/<int:id>',PatientCosts.as_view(),name='patient-costs'),
    path('<str:mode>/<int:prami>',Patients.as_view(),name='patients'),
    path('<str:mode>',Patients.as_view(),name='patients-no-num'),
]
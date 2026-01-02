from django.urls import path
from .views import CSVValidateView,BulkHospitalCreateView,app_home

urlpatterns =[
    path('',app_home,name='home'),
    path('hospitals/bulk/validate', CSVValidateView.as_view()),
    path('hospitals/bulk', BulkHospitalCreateView.as_view()),
]
from django.urls import path
#from .views import chirri_home
from .views import CSVValidateView,BulkHospitalCreateView

urlpatterns =[
    path('hospitals/bulk/validate', CSVValidateView.as_view()),
    path('hospitals/bulk', BulkHospitalCreateView.as_view()),
]
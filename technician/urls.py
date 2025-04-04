from django.urls import path, include

from .views import (
    TechniciansTableView,
    TechnicianCreateView,
    TechnicianUpdateView,
    TechnicianDeleteView,
)

app_name = 'technician'
urlpatterns = [
    path('', TechniciansTableView.as_view(), name='table-technicians'),
    path('create/', TechnicianCreateView.as_view(), name='create-technician'),
    path('update/<int:pk>', TechnicianUpdateView.as_view(), name='update-technician'),
    path('delete/<int:pk>', TechnicianDeleteView.as_view(), name='delete-technician'),
]

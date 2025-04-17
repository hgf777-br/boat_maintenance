from django.urls import path

from .views import (
    MaintenancesPendingTableView,
    MaintenancesFinishedTableView,
    MaintenanceDetailsView,
    MaintenanceCreateView,
    MaintenanceUpdateView,
    MaintenanceDeleteView,
    MaintenanceFlowView,
    PeriodicCreateView,
    PeriodicDeleteView,
    PeriodicUpdateView,
    PeriodicsTableView,
    PeriodicDetailsView,
)

app_name = 'maintenance'
urlpatterns = [
    path('', MaintenancesPendingTableView.as_view(), name='table-pending-maintenances'),
    path('finished/', MaintenancesFinishedTableView.as_view(), name='table-finished-maintenances'),
    path('<int:pk>', MaintenanceDetailsView.as_view(), name='details-maintenance'),
    path('create/', MaintenanceCreateView.as_view(), name='create-maintenance'),
    path('update/<int:pk>', MaintenanceUpdateView.as_view(), name='update-maintenance'),
    path('delete/<int:pk>', MaintenanceDeleteView.as_view(), name='delete-maintenance'),
    path('flow', MaintenanceFlowView.as_view(), name='flow-maintenance'),
    path('periodic/', PeriodicsTableView.as_view(), name='table-periodics'),
    path('periodic/<int:pk>', PeriodicDetailsView.as_view(), name='details-periodic'),
    path('periodic/create/', PeriodicCreateView.as_view(), name='create-periodic'),
    path('periodic/update/<int:pk>', PeriodicUpdateView.as_view(), name='update-periodic'),
    path('periodic/delete/<int:pk>', PeriodicDeleteView.as_view(), name='delete-periodic'),
]

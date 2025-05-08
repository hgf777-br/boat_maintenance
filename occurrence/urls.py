from django.urls import path

from .views import (
    OccurrenceCreateView,
    OccurrenceDeleteView,
    OccurrenceUpdateView,
    OccurrencesTableView,
    OccurrenceCreateMaintenanceView,
    CheckInOutsTableView,
    CheckInOutCreateView,
    CheckInOutUpdateView,
    CheckInOutDeleteView,  # Create a check-in/check-out for an occurrence. This is a POST request.
)

app_name = 'occurrence'
urlpatterns = [
    path('occurrence/', OccurrencesTableView.as_view(), name='table-occurrences'),
    path('occurrence/create/', OccurrenceCreateView.as_view(), name='create-occurrence'),
    path('occurrence/update/<int:pk>', OccurrenceUpdateView.as_view(), name='update-occurrence'),
    path('occurrence/delete/<int:pk>', OccurrenceDeleteView.as_view(), name='delete-occurrence'),
    path(
        'occurrence/create-maintenance/',
        OccurrenceCreateMaintenanceView.as_view(),
        name='create-maintenance-occurrence'
        ),
    path('check_in_out/', CheckInOutsTableView.as_view(), name='table-check-in-outs'),
    path('check_in_out/create/', CheckInOutCreateView.as_view(), name='create-check-in-out'),
    path('check_in_out/update/<int:pk>', CheckInOutUpdateView.as_view(), name='update-check-in-out'),
    path('check_in_out/delete/<int:pk>', CheckInOutDeleteView.as_view(), name='delete-check-in-out'),
]

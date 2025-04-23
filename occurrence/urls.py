from django.urls import path

from .views import (
    OccurrenceCreateView,
    OccurrenceDeleteView,
    OccurrenceUpdateView,
    OccurrencesTableView,
    OccurrenceCreateMaintenanceView,  # Create a maintenance for an occurrence. This is a POST request.
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
]

from django.urls import path, include

from .views import (
   BoatsTableView,
   BoatCreateView,
   BoatUpdateView,
   BoatDeleteView,
   BoatDetailsListView,
   BoatUpdateOwnersView,
)

app_name = 'boat'
urlpatterns = [
    path('', BoatsTableView.as_view(), name='table-boats'),
    path('create/', BoatCreateView.as_view(), name='create-boat'),
    path('update/<int:pk>', BoatUpdateView.as_view(), name='update-boat'),
    path('delete/<int:pk>', BoatDeleteView.as_view(), name='delete-boat'),
    path('update_owners/', BoatUpdateOwnersView.as_view(), name='update-owners-boat'  ),
    path('details_list/', BoatDetailsListView.as_view(), name='details-list-boat'),
]

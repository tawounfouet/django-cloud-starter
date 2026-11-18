from django.urls import path

from .views import (
    RecordCreateView,
    RecordDeleteView,
    RecordDetailView,
    RecordListView,
    RecordUpdateView,
)

urlpatterns = [
    path("", RecordListView.as_view(), name="record_list"),
    path("new/", RecordCreateView.as_view(), name="record_create"),
    path("<int:pk>/", RecordDetailView.as_view(), name="record_detail"),
    path("<int:pk>/edit/", RecordUpdateView.as_view(), name="record_update"),
    path("<int:pk>/delete/", RecordDeleteView.as_view(), name="record_delete"),
]

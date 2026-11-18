from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("records/", include("apps.records.urls")),
    path("admin/", admin.site.urls),
]

from django.urls import path, include

app_name = "core"
urlpatterns = [
    path("api/", include("dialog_apps.core.api.urls")),
]
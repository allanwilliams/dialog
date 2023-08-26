from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
urlpatterns = []

urlpatterns += [
    path('general/', include('dialog_apps.core.api.urls_generals')),
]


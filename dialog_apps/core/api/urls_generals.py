from rest_framework.routers import DefaultRouter
from .viewsets import GeneralViewSet, GetModelViewSet, GetLabelViewSet

router = DefaultRouter()
# router.register(r'get-label', GetLabelViewSet, basename='get-label')
# router.register(r'(?P<app_label>\w+)/get-model', GetModelViewSet, basename='get-model')
# router.register(r'(?P<app_label>\w+)/(?P<model_name>\w+)(?:/(?P<id>\w+))?', GeneralViewSet, basename='general')
router.register(r'(?P<app_label>\w+)/(?P<model_name>\w+)(?:/(?P<id>\.+))?', GeneralViewSet, basename='general')



print('urls generals',router.urls)

urlpatterns = router.urls

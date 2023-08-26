from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import GenericAllSerializer
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class ResultsSetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 200
    

class GeneralSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1
    def get_page_size(self, request):
        if request.GET.get('paginator'):
            return 2000
        else:
            return 20

class GeneralViewSet(ModelViewSet):
    pagination_class = GeneralSetPagination
    permission_classes = []
    http_method_names = ['get','post','patch','put','delete']

    @property
    def model(self):
        print('self',self.kwargs['model_name'])
        try:
            return apps.get_model(app_label=str(self.kwargs['app_label']), model_name=str(self.kwargs['model_name']))
        except:
            return None
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
   
    def create(self, request, *args, **kwargs):
        create_dict = request.data
        obj = self.model(**create_dict)
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def valida_permissao(self,user,model):
        return True
        if not user.is_superuser:
            if model._meta.db_table in ['certidao_localizacao_certidao','session_userpage']:
                return True
            if user.has_perm(f'{app_label}.view_{model_name.lower()}'):
                return True
            return False
        return True
    
    def get_paginated_response(self, data):
        id = self.kwargs.get('id')
        if id:
            return Response(data[0],status=status.HTTP_200_OK)
        return super().get_paginated_response(data)
    
    def get_queryset(self):
        if self.model:
            model = self.model
            id = self.kwargs.get('id')
        
            print('id',self)
            if id:
                if self.valida_permissao(user=self.request.user,model=model):
                    return model.objects.filter(pk=id)
                else:
                    return []
                    
            if self.request.GET:
                result = model.objects.filter(pk__gte=0)
                for param in self.request.GET:
                    value = self.request.GET.get(param)
                    param = param + '__icontains' if self.request.GET.get('icontains') else param
                    try:
                        result = result.filter(**{ param:value })
                    except: pass
                if self.valida_permissao(user=self.request.user,model=model):
                    return result
                return []
            if self.valida_permissao(user=self.request.user,model=model):
                return model.objects.all()
        return []

    def get_serializer_class(self):
        GenericAllSerializer.Meta.model = self.model
        return GenericAllSerializer
    
class GetLabelViewSet(GenericViewSet):
    pagination_class = GeneralSetPagination
    permission_classes = []
    http_method_names = ['get']
    def get_queryset(self):
        return None
    
    def list(self, request):
        from django.conf import settings
        local_apps = [{ 'app_label': a, 'url': f"/main/api/general/{a}/get-model" } for a in settings.LOCAL_APPS]
        return Response({'mensagem': 'Sucesso', 'results': local_apps}, status=status.HTTP_200_OK)

class GetModelViewSet(GenericViewSet):
    pagination_class = GeneralSetPagination
    permission_classes = []
    http_method_names = ['get']
    
    def get_queryset(self):
        return None
    
    def list(self,request,app_label):
        app_models = [{'app_model':m.__name__, 'url': f"/main/api/general/{app_label}/{m.__name__}" } for m in apps.get_app_config(app_label).get_models()]
        return Response({'mensagem': 'Sucesso', 'results': app_models}, status=status.HTTP_200_OK)
from django.db import models
from django_currentuser.middleware import get_current_user
from django.contrib.auth.models import User
from django.utils import timezone

TIPO_VIDEO_ARQUIVO = "Arquivo"
TIPO_VIDEO_URL = "URL"

CHOICES_TIPO_VIDEO = (
    (1,TIPO_VIDEO_ARQUIVO),
    (2,TIPO_VIDEO_URL)
)


class BaseModel(models.Model):
    criado_em = models.DateTimeField(blank=True, null=True)
    criado_por = models.ForeignKey(User,
                                   on_delete=models.DO_NOTHING,
                                   related_name='%(class)s_criado_por',
                                   blank=True,
                                   null=True,
                                   default=get_current_user())
    modificado_em = models.DateTimeField(blank=True, null=True)
    modificado_por = models.ForeignKey(User,
                                       on_delete=models.DO_NOTHING,
                                       related_name='%(class)s_modificado_por',
                                       blank=True,
                                       null=True)

    class Meta:
        abstract = True

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if get_current_user():
            if (not self.criado_por or not self.criado_em) and get_current_user() and get_current_user().id:
                self.criado_por = get_current_user()
                self.criado_em = timezone.now()
            elif get_current_user() and get_current_user().id:
                self.modificado_por = get_current_user()
                self.modificado_em = timezone.now()
        super(BaseModel, self).save(force_insert=False,
                                    force_update=False,
                                    using=None,
                                    update_fields=None)
        
class Post(BaseModel):
    autor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mensagem = models.TextField()
    imagem = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    tipo_video = models.CharField(choices=CHOICES_TIPO_VIDEO,blank=True,null=True)
    arquivo_video = models.FileField(upload_to=None, max_length=100,blank=True,null=True)
    url_video = models.CharField(max_length=500,blank=True,null=True)

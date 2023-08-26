from django.db import models
from django_currentuser.middleware import get_current_user
from django.contrib.auth.models import User
from django.utils import timezone

TIPO_VIDEO_ARQUIVO = "VÍDEO"
TIPO_VIDEO_URL = "URL"
TIPO_IMAGEM = "IMAGEM"

CHOICES_TIPO_MEDIA = (
    (TIPO_VIDEO_ARQUIVO,TIPO_VIDEO_ARQUIVO),
    (TIPO_VIDEO_URL,TIPO_VIDEO_URL),
    (TIPO_IMAGEM, TIPO_IMAGEM)
)

TIPO_PESQUISA_QUIZ = "QUIZ"
TIPO_PESQUISA_PESQUISA = "PESQUISA"

CHOICES_TIPO_PESQUISA = (
    (TIPO_PESQUISA_QUIZ, TIPO_PESQUISA_QUIZ),
    (TIPO_PESQUISA_PESQUISA, TIPO_PESQUISA_PESQUISA),
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
    agendado = models.BooleanField(default=False)
    data_agendado = models.DateField(blank=True,null=True)
    imagem = models.ImageField(upload_to='store/core/posts/', height_field=None, width_field=None, max_length=None)
    permite_curtida = models.BooleanField(default=True)
    permite_comentario = models.BooleanField(default=True)
    
class PostComentario(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mensagem = models.TextField()
    
class PostCurtida(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)    

class Galeria(BaseModel):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    permite_curtida = models.BooleanField(default=True)
    permite_comentario = models.BooleanField(default=True)

class GaleriaMedia(BaseModel):
    nome = models.CharField(max_length=50)
    arquivo = models.FileField(upload_to='store/core/galeria/', max_length=100)
    tipo = models.CharField(max_length=50, choices=CHOICES_TIPO_MEDIA)
    link = models.CharField(max_length=500, null=True, blank=True)
    galeria = models.ForeignKey(Galeria, on_delete=models.DO_NOTHING)
    
class GaleriaMediaComentario(BaseModel):
    galeria_media = models.ForeignKey(GaleriaMedia, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mensagem = models.TextField()
    
class GaleriaMediaCurtida(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)    

class Cargo(BaseModel):
    nome = models.CharField(max_length=50)
    
class Departamento(BaseModel):
    nome = models.CharField(max_length=50)
    lider = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='%(class)s_lider')
    defensor_lider = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='%(class)s_defensor_lider')
    
class Pesquisa(BaseModel):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=CHOICES_TIPO_PESQUISA)
    
    def __str__(self):
        return self.titulo
    
class PesquisaPergunta(BaseModel):
    pergunta = models.TextField()
    pesquisa = models.ForeignKey(Pesquisa,on_delete=models.DO_NOTHING)
class PesquisaPerguntaAlternativa(BaseModel):
    texto = models.TextField()
    pergunta = models.ForeignKey(PesquisaPergunta,on_delete=models.DO_NOTHING, blank=True, null=True)
    is_correta = models.BooleanField(default=False)
    
class PesquisaResposta(BaseModel):
    pergunta = models.ForeignKey(PesquisaPergunta,on_delete=models.DO_NOTHING,related_name='%(class)s_pergunta')
    alternativa = models.ForeignKey(PesquisaPerguntaAlternativa,on_delete=models.DO_NOTHING,related_name='%(class)s_alternativa')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='%(class)s_lider')
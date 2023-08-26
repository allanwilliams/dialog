from django.contrib import admin
from .models import Galeria, Cargo, Departamento, GaleriaMedia, Post, Pesquisa, PesquisaPergunta, PesquisaPerguntaAlternativa


class GaleriaMediaInline(admin.StackedInline):
    model = GaleriaMedia
    extra = 1
    fields = (
        'tipo',
        'arquivo',
        'link'
    )

class PesquisaPerguntaAlternativaInline(admin.StackedInline):
    model = PesquisaPerguntaAlternativa
    extra = 1
    
    fields = (
        'texto',
        'is_correta'
    )
class PesquisaPerguntaInline(admin.StackedInline):
    model = PesquisaPergunta
    extra = 1
    fields = (
        'pergunta',
    )
    
    inlines = [
        PesquisaPerguntaAlternativa
    ]
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    
    fields = [
        'mensagem',
        'agendado',
        'data_agendado',
        'imagem',
        'permite_curtida',
        'permite_comentario',
    ]

@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    model = Galeria
    
    fields = [
        'nome',
        'descricao',
        'permite_curtida',
        'permite_comentario',
    ]
    
    inlines = [
        GaleriaMediaInline
    ]
    
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    model = Cargo
    
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    model = Departamento
    
@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    model = Pesquisa
    fields = [
        'titulo',
        'descricao',
        'tipo'
    ]
    
    inlines = [
        PesquisaPerguntaInline
    ]
    
@admin.register(PesquisaPergunta)
class PesquisaPerguntaAdmin(admin.ModelAdmin):
    model = PesquisaPergunta
    
    inlines = [
        PesquisaPerguntaAlternativaInline
    ]
# Generated by Django 3.2 on 2023-05-22 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230522_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galeriamedia',
            name='tipo',
            field=models.CharField(choices=[('VÍDEO', 'VÍDEO'), ('URL', 'URL'), ('IMAGEM', 'IMAGEM')], max_length=50),
        ),
        migrations.AlterField(
            model_name='pesquisa',
            name='tipo',
            field=models.CharField(choices=[('QUIZ', 'QUIZ'), ('PESQUISA', 'PESQUISA')], max_length=50),
        ),
        migrations.AlterField(
            model_name='pesquisaperguntaalternativa',
            name='pergunta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.pesquisapergunta'),
        ),
    ]

# Generated by Django 3.2 on 2023-05-25 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_galeriamedia_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galeriamedia',
            name='link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]

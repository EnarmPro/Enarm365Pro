# Generated by Django 4.2.13 on 2024-06-17 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_cantidadpagos_cantidadpago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntas',
            name='tipoPregunta',
            field=models.TextField(default='Aleatoria'),
        ),
    ]

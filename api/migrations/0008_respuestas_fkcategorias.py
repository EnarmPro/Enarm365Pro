# Generated by Django 4.2.13 on 2024-05-14 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_preguntas_fktemarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestas',
            name='fkCategorias',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.categorias'),
        ),
    ]

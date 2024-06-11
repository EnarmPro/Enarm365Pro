# Generated by Django 4.2.13 on 2024-06-11 20:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_preguntas_respuesta_incorrecta_dos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanelInformation',
            fields=[
                ('idPanel', models.AutoField(primary_key=True, serialize=False)),
                ('titlePanel', models.TextField()),
                ('fechaPanel', models.DateField(default=datetime.date.today)),
                ('texto_uno', models.TextField()),
                ('tituloPanel_dos', models.TextField()),
                ('texto_dos', models.TextField()),
                ('tituloPanel_tres', models.TextField()),
                ('texto_tres', models.TextField()),
            ],
            options={
                'db_table': 'PanelInformation',
            },
        ),
    ]

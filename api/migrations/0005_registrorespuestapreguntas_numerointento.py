# Generated by Django 4.2.13 on 2024-05-13 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_preguntas_nivelpregunta_preguntas_nombretema'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrorespuestapreguntas',
            name='numeroIntento',
            field=models.IntegerField(default=1),
        ),
    ]

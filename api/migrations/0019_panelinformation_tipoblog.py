# Generated by Django 4.2.13 on 2024-06-11 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_panelinformation_texto_referencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='panelinformation',
            name='tipoBlog',
            field=models.TextField(default=''),
        ),
    ]

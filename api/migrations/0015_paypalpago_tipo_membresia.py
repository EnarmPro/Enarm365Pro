# Generated by Django 4.2.13 on 2024-06-06 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_paypalpago'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalpago',
            name='tipo_membresia',
            field=models.CharField(default='', max_length=255),
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-18 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juapp', '0016_auto_20200218_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagina',
            name='creado_em',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
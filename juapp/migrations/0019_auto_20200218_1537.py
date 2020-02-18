# Generated by Django 3.0.3 on 2020-02-18 18:37

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('juapp', '0018_auto_20200218_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diario',
            name='baixado_em',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='diario',
            name='data',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='diario',
            name='procurado_em',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pagina',
            name='criado_em',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='termoparabusca',
            name='desde',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
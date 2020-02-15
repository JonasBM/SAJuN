# Generated by Django 3.0.3 on 2020-02-12 14:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('quantidade_total', models.IntegerField()),
                ('data', models.DateField(blank=True, default=datetime.datetime.now)),
                ('baixado_em', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('procurado_em', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['local_para_busca', 'data'],
            },
        ),
        migrations.CreateModel(
            name='LocalParaBusca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('dias_para_busca', models.PositiveSmallIntegerField(db_index=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='TermosParaBusca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.CharField(max_length=255)),
                ('local_para_busca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='termos_para_busca', to='juapp.LocalParaBusca')),
            ],
            options={
                'ordering': ['local_para_busca', 'string'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagina', models.IntegerField()),
                ('quantidade', models.IntegerField()),
                ('diario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='juapp.Diario')),
            ],
            options={
                'ordering': ['diario', 'pagina'],
            },
        ),
        migrations.CreateModel(
            name='HorarioDeBusca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.TimeField()),
                ('local_para_busca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_para_busca', to='juapp.LocalParaBusca')),
            ],
            options={
                'ordering': ['local_para_busca', 'horario'],
            },
        ),
        migrations.AddField(
            model_name='diario',
            name='local_para_busca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diarios', to='juapp.LocalParaBusca'),
        ),
        migrations.AddField(
            model_name='diario',
            name='termos_buscados',
            field=models.ManyToManyField(related_name='diarios', to='juapp.TermosParaBusca'),
        ),
    ]

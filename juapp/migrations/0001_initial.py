# Generated by Django 3.0.3 on 2020-02-19 16:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('url', models.URLField()),
                ('data', models.DateField(default=datetime.date.today)),
                ('baixado_em', models.DateTimeField(default=django.utils.timezone.now)),
                ('procurado_em', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0))),
            ],
            options={
                'ordering': ['local_para_busca', 'data'],
            },
        ),
        migrations.CreateModel(
            name='LocalParaBusca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('logo', models.URLField(blank=True, null=True)),
                ('method', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Locais para busca',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='TermoParaBusca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.CharField(max_length=255)),
                ('desde', models.DateField(blank=True, default=datetime.date.today)),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now)),
                ('local_para_busca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='termos_para_busca', to='juapp.LocalParaBusca')),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='termos_para_busca', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Termos para busca',
                'ordering': ['local_para_busca', 'string'],
            },
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagina', models.IntegerField()),
                ('quantidade', models.IntegerField()),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now)),
                ('diario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paginas', to='juapp.Diario')),
                ('termo_buscado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paginas', to='juapp.TermoParaBusca')),
            ],
            options={
                'ordering': ['diario', 'pagina'],
            },
        ),
        migrations.AddField(
            model_name='diario',
            name='local_para_busca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diarios', to='juapp.LocalParaBusca'),
        ),
    ]

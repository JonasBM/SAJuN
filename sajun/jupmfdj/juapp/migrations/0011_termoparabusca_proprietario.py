# Generated by Django 3.0.3 on 2020-02-16 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('juapp', '0010_remove_termoparabusca_proprietario'),
    ]

    operations = [
        migrations.AddField(
            model_name='termoparabusca',
            name='proprietario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='termos_para_busca', to=settings.AUTH_USER_MODEL),
        ),
    ]
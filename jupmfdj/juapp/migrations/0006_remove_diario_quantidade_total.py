# Generated by Django 3.0.3 on 2020-02-13 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juapp', '0005_auto_20200212_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diario',
            name='quantidade_total',
        ),
    ]

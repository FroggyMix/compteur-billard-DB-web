# Generated by Django 3.0.5 on 2020-05-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0033_auto_20200527_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeuvariantes',
            name='ordre',
            field=models.SmallIntegerField(default=1, help_text='Ordre dans lequel les variantes seront affichées', verbose_name="Ordre d'affichage"),
        ),
    ]

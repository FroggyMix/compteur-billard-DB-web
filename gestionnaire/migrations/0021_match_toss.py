# Generated by Django 3.0.5 on 2020-05-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0020_auto_20200502_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='toss',
            field=models.SmallIntegerField(default=1, help_text='Saisir 1 ouu 2 en fonction du joueur qui commence', verbose_name='Joueur qui débutera'),
        ),
    ]

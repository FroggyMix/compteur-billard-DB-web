# Generated by Django 3.0.5 on 2020-04-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0013_auto_20200429_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frame',
            name='en_cours',
        ),
        migrations.AddField(
            model_name='frame',
            name='status',
            field=models.CharField(choices=[('cree', 'Creé'), ('prevu', 'Prévu/Planifié'), ('en_cours', 'En cours'), ('termine', 'Terminé')], default='cree', max_length=20),
        ),
    ]

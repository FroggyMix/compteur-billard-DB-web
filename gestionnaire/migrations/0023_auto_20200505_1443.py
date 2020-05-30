# Generated by Django 3.0.5 on 2020-05-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0022_auto_20200504_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='distanceFR_j1',
            new_name='fr_distance_j1',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='distanceFR_j2',
            new_name='fr_distance_j2',
        ),
        migrations.AddField(
            model_name='match',
            name='fr_limite_nb_reprises',
            field=models.SmallIntegerField(blank=True, default=30, help_text='Optionnel, ne concerne que la carambole', null=True, verbose_name='Limite du nombre de reprises'),
        ),
        migrations.AddField(
            model_name='match',
            name='fr_reprise_egalisatrice',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='d_debut',
            field=models.DateTimeField(blank=True, help_text='laissez la valeur par défaut pour un démarrage immédiat', null=True, verbose_name='Début du match'),
        ),
    ]
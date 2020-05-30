# Generated by Django 3.0.5 on 2020-05-07 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0023_auto_20200505_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='frame',
            options={'ordering': ['-match__id', '-num'], 'verbose_name_plural': 'FrameModel'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-pk'], 'verbose_name_plural': 'MatchModel'},
        ),
        migrations.AlterField(
            model_name='match',
            name='d_debut',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Début réel du match'),
        ),
        migrations.AlterField(
            model_name='match',
            name='d_fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fin réel du match'),
        ),
        migrations.AlterField(
            model_name='match',
            name='fr_distance_j1',
            field=models.SmallIntegerField(blank=True, default=10, help_text='Optionnel, ne concerne que la carambole', null=True, verbose_name='Distance joueur 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='fr_distance_j2',
            field=models.SmallIntegerField(blank=True, default=10, help_text='Optionnel, ne concerne que la carambole', null=True, verbose_name='Distance joueur 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='fr_limite_nb_reprises',
            field=models.SmallIntegerField(blank=True, default=10, help_text='Optionnel, ne concerne que la carambole', null=True, verbose_name='Limite du nombre de reprises'),
        ),
        migrations.AlterField(
            model_name='match',
            name='jeu_variante',
            field=models.ForeignKey(db_column='Jeu_Variantes_id', default=5, on_delete=django.db.models.deletion.PROTECT, to='gestionnaire.JeuVariantes', verbose_name='Variante de jeu'),
        ),
        migrations.AlterField(
            model_name='match',
            name='joueur1',
            field=models.ForeignKey(db_column='joueur1_id', default=1, on_delete=django.db.models.deletion.PROTECT, related_name='joueur1', to='gestionnaire.Joueur', verbose_name='Joueur 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='joueur2',
            field=models.ForeignKey(db_column='joueur2_id', default=1, on_delete=django.db.models.deletion.PROTECT, related_name='joueur2', to='gestionnaire.Joueur', verbose_name='Joueur 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='nb_frames',
            field=models.SmallIntegerField(default=3, help_text='Nombre de frames maximum à jouer dans ce match', verbose_name='Nombre de frames'),
        ),
    ]
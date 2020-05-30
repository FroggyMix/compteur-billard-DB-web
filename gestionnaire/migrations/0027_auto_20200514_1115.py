# Generated by Django 3.0.5 on 2020-05-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0026_frameevent_origine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frameevent',
            name='origine',
            field=models.CharField(choices=[('system', 'Système'), ('user', 'Utilisateur'), ('ia-image', 'IA-image'), ('ia-son', 'IA-son')], default='system', max_length=15, verbose_name="Origine de l'enregistrement"),
        ),
    ]

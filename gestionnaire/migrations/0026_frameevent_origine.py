# Generated by Django 3.0.5 on 2020-05-14 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0025_auto_20200509_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='frameevent',
            name='origine',
            field=models.CharField(blank=True, choices=[('system', 'Système'), ('user', 'Utilisateur'), ('ia-image', 'IA-image'), ('ia-son', 'IA-son')], default='system', max_length=15, null=True, verbose_name="Origine de l'enregistrement"),
        ),
    ]

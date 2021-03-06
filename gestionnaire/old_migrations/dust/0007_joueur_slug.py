# Generated by Django 3.0.4 on 2020-04-15 15:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0006_remove_joueur_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='joueur',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-15 14:23

from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0003_auto_20200415_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frame',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='joueur',
            name='slug',
        ),
    ]

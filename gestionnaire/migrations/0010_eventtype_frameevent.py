# Generated by Django 3.0.5 on 2020-04-27 09:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0009_auto_20200423_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=32, unique=True)),
                ('jeu_type', models.CharField(blank=True, choices=[('fr', 'Carambole'), ('sn', 'Snooker'), ('po', 'Pool'), ('us', 'Américain')], default='fr', max_length=2)),
                ('description', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'verbose_name_plural': 'EventTypeModel',
                'db_table': 'EventType',
            },
        ),
        migrations.CreateModel(
            name='FrameEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_horodatage', models.DateTimeField(default=django.utils.timezone.now)),
                ('crediteur', models.SmallIntegerField()),
                ('points', models.SmallIntegerField()),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestionnaire.EventType')),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestionnaire.Frame')),
            ],
            options={
                'verbose_name_plural': 'FrameEventModel',
                'db_table': 'FrameEvent',
                'ordering': ['-d_horodatage'],
            },
        ),
    ]

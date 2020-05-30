# Generated by Django 3.0.5 on 2020-05-09 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0024_auto_20200507_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frame',
            name='match',
            field=models.ForeignKey(db_column='Match_id', on_delete=django.db.models.deletion.CASCADE, to='gestionnaire.Match'),
        ),
        migrations.AlterField(
            model_name='frameevent',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionnaire.Frame'),
        ),
    ]

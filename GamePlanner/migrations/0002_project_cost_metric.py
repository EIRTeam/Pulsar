# Generated by Django 2.0.5 on 2018-05-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cost_metric',
            field=models.CharField(choices=[('HOURS', 'Hours'), ('DAYS', 'Days'), ('POINTS', 'Points')], default='HOURS', max_length=2),
        ),
    ]

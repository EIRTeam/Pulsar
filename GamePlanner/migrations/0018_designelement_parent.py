# Generated by Django 2.0.5 on 2018-05-18 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlanner', '0017_auto_20180518_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='designelement',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='GamePlanner.DesignElement'),
        ),
    ]

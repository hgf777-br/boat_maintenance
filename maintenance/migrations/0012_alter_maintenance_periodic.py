# Generated by Django 5.1.7 on 2025-04-04 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0011_maintenance_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='periodic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maintenance.periodic', verbose_name='periodic'),
        ),
    ]

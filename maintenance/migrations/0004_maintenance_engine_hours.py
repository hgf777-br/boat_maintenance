# Generated by Django 5.1.7 on 2025-03-30 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_alter_maintenance_boat_alter_maintenance_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='engine_hours',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='engine hours'),
        ),
    ]

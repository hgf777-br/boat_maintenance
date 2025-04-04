# Generated by Django 5.1.7 on 2025-03-23 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boat', '0005_remove_boat_manufactor_boat_created_at_and_more'),
        ('technician', '0002_technician_created_at_technician_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256, verbose_name='description')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('schedule_date', models.DateField(blank=True, null=True, verbose_name='schedule date')),
                ('observation', models.TextField(blank=True, verbose_name='observation')),
                ('finish_date', models.DateField(blank=True, null=True, verbose_name='finish date')),
                ('completed', models.BooleanField(default=False, verbose_name='completed')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boat.boat', verbose_name='boat')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technician.technician', verbose_name='technician')),
            ],
        ),
    ]

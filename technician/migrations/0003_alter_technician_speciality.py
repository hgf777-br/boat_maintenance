# Generated by Django 5.1.7 on 2025-03-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technician', '0002_technician_created_at_technician_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='speciality',
            field=models.CharField(choices=[('ME', 'mechanic'), ('PL', 'plumber'), ('EL', 'electrician'), ('CA', 'carpenter'), ('PA', 'painter'), ('UP', 'upholsterer'), ('EN', 'engineer'), ('OT', 'other')], default='ME', max_length=2, verbose_name='speciality'),
        ),
    ]

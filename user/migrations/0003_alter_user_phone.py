# Generated by Django 5.1.7 on 2025-03-22 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=16, verbose_name='cell phone'),
        ),
    ]

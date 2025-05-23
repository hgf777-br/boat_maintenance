# Generated by Django 5.1.7 on 2025-03-30 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0005_remove_boat_manufactor_boat_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='manufacturer',
            field=models.CharField(choices=[('Fast', 'Fast'), ('Delta', 'Delta'), ('Beneteau', 'Beneteau'), ('Jenneau', 'Jenneau'), ('MJ', 'MJ')], default='Fast', max_length=64, verbose_name='manufacturer'),
        ),
    ]

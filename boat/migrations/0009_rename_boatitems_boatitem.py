# Generated by Django 5.2 on 2025-04-10 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0008_boatitems_item_boat_items'),
        ('occurrence', '0003_alter_item_sector_alter_occurrence_sector'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BoatItems',
            new_name='BoatItem',
        ),
    ]

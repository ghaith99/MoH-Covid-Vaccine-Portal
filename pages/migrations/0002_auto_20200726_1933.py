# Generated by Django 3.0 on 2020-07-26 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Citizen',
            new_name='Patient',
        ),
    ]
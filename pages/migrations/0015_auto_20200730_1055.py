# Generated by Django 3.0 on 2020-07-30 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_test_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='sampling_datetime',
            new_name='sample_datetime',
        ),
    ]
# Generated by Django 3.0 on 2020-07-29 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20200729_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='created_datetime',
        ),
        migrations.AlterField(
            model_name='test',
            name='mixed',
            field=models.CharField(blank=True, choices=[('False', 'False'), ('True', 'True')], default='False', max_length=10, null=True, verbose_name='Mixed'),
        ),
        migrations.AlterField(
            model_name='test',
            name='sampling_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Sampling Date'),
        ),
        migrations.AlterField(
            model_name='test',
            name='symptoms',
            field=models.CharField(blank=True, choices=[('False', 'False'), ('True', 'True')], default='False', max_length=10, null=True, verbose_name='Covid Symptoms'),
        ),
    ]
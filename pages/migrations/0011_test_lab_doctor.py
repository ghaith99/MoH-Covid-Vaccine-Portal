# Generated by Django 3.0 on 2020-07-29 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20200729_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='lab_doctor',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Lab Doctor'),
        ),
    ]
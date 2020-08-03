# Generated by Django 3.0 on 2020-08-03 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0004_auto_20200803_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='completed',
        ),
        migrations.AlterField(
            model_name='test',
            name='lab_doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_doctor', to=settings.AUTH_USER_MODEL, verbose_name='Lab Doctor'),
        ),
    ]
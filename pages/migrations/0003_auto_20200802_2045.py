# Generated by Django 3.0 on 2020-08-02 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0002_auto_20200802_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='test',
            name='field_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_user', to=settings.AUTH_USER_MODEL, verbose_name='Field User'),
        ),
        migrations.AlterField(
            model_name='test',
            name='lab_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_user', to=settings.AUTH_USER_MODEL, verbose_name='Lab User'),
        ),
        migrations.AlterField(
            model_name='test',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_tests', to='pages.Patient', verbose_name='Patient Civil ID'),
        ),
        migrations.AlterField(
            model_name='test',
            name='screening_center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='screeningcenter_tests', to='pages.ScreeningCenter', verbose_name='Screening Center'),
        ),
        migrations.AlterField(
            model_name='test',
            name='testing_center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testingcenter_tests', to='pages.TestingCenter', verbose_name='Testing Center'),
        ),
    ]

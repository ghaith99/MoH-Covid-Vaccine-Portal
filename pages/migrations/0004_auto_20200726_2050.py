# Generated by Django 3.0 on 2020-07-26 17:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0003_auto_20200726_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='allergy',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Allergy'),
        ),
        migrations.AddField(
            model_name='patient',
            name='alzheimer',
            field=models.BooleanField(blank=True, null=True, verbose_name='Alzheimer'),
        ),
        migrations.AddField(
            model_name='patient',
            name='asthma',
            field=models.BooleanField(blank=True, null=True, verbose_name='Asthma'),
        ),
        migrations.AddField(
            model_name='patient',
            name='bloodType',
            field=models.CharField(blank=True, choices=[('A+', 'A+ Type'), ('B+', 'B+ Type'), ('AB+', 'AB+ Type'), ('O+', 'O+ Type'), ('A-', 'A- Type'), ('B-', 'B- Type'), ('AB-', 'AB- Type'), ('O-', 'O- Type')], max_length=10, null=True, verbose_name='Blood Type'),
        ),
        migrations.AddField(
            model_name='patient',
            name='comments',
            field=models.TextField(blank=True, max_length=700, null=True, verbose_name='Comments'),
        ),
        migrations.AddField(
            model_name='patient',
            name='diabetes',
            field=models.BooleanField(blank=True, null=True, verbose_name='Diabetes'),
        ),
        migrations.AddField(
            model_name='patient',
            name='stroke',
            field=models.BooleanField(blank=True, null=True, verbose_name='Stroke'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='city',
            field=models.CharField(max_length=25, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='civilID',
            field=models.CharField(max_length=25, verbose_name='Civil ID'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='civilSerial',
            field=models.CharField(max_length=25, verbose_name='Civil Serial'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='firstname',
            field=models.CharField(max_length=25, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='lastname',
            field=models.CharField(max_length=25, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='symptoms',
            field=models.TextField(blank=True, max_length=250, verbose_name='Symptoms'),
        ),
        migrations.AlterField(
            model_name='test',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='test',
            name='completed',
            field=models.BooleanField(blank=True, null=True, verbose_name='Completed'),
        ),
        migrations.AlterField(
            model_name='test',
            name='datatime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Created Data time'),
        ),
        migrations.AlterField(
            model_name='test',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Hospital', verbose_name='Hospital'),
        ),
        migrations.AlterField(
            model_name='test',
            name='lastModified',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='test',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='test',
            name='resultDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Result Date'),
        ),
        migrations.AlterField(
            model_name='test',
            name='testNotes',
            field=models.TextField(verbose_name='Test Notes'),
        ),
        migrations.AlterField(
            model_name='test',
            name='testResult',
            field=models.NullBooleanField(choices=[(None, ''), (True, 'Yes'), (False, 'No')], default=None, max_length=3, verbose_name='Test Result'),
        ),
        migrations.DeleteModel(
            name='MedicalInfo',
        ),
    ]
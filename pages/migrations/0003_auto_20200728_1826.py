# Generated by Django 3.0 on 2020-07-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20200728_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='testResult',
            field=models.CharField(blank=True, choices=[(None, ''), ('Positive', 'Positive'), ('Negative', 'Negative'), ('Equivalent', 'Equivalent'), ('Reject', 'Reject')], default=None, max_length=10, null=True, verbose_name='Test Result'),
        ),
    ]
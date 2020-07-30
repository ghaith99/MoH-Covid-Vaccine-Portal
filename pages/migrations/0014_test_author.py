# Generated by Django 3.0 on 2020-07-30 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0013_test_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
            preserve_default=False,
        ),
    ]
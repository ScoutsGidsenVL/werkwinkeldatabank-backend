# Generated by Django 3.1 on 2020-10-01 11:26

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0010_auto_20201001_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingblockinstance',
            name='_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buildingblockinstance',
            name='_duration',
            field=models.DurationField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.timedelta(seconds=60)), django.core.validators.MaxValueValidator(datetime.timedelta(days=1))]),
        ),
        migrations.AlterField(
            model_name='buildingblockinstance',
            name='_is_sensitive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

# Generated by Django 3.1.2 on 2021-02-22 08:57

import datetime

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workshops", "0032_auto_20201021_1336"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingblocktemplate",
            name="last_edited",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="buildingblockinstance",
            name="_duration",
            field=models.DurationField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(datetime.timedelta(0)),
                    django.core.validators.MaxValueValidator(datetime.timedelta(days=1)),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="buildingblocktemplate",
            name="duration",
            field=models.DurationField(
                validators=[
                    django.core.validators.MinValueValidator(datetime.timedelta(0)),
                    django.core.validators.MaxValueValidator(datetime.timedelta(days=1)),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]

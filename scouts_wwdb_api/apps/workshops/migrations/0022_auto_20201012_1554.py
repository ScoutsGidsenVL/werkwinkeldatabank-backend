# Generated by Django 3.1 on 2020-10-12 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0021_merge_20201012_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshop',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

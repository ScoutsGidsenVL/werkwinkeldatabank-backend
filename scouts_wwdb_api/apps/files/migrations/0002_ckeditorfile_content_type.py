# Generated by Django 3.1 on 2020-10-07 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ckeditorfile',
            name='content_type',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]

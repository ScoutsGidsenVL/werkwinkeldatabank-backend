# Generated by Django 3.1 on 2020-09-04 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0008_auto_20200902_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingblockinstance',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='workshops.theme'),
        ),
        migrations.AddField(
            model_name='buildingblocktemplate',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='workshops.theme'),
        ),
    ]
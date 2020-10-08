# Generated by Django 3.1 on 2020-10-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0009_auto_20201001_0729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='buildingblock_necessities',
            new_name='_buildingblock_necessities',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='category',
            new_name='_category',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='description',
            new_name='_description',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='duration',
            new_name='_duration',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='is_sensitive',
            new_name='_is_sensitive',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='order',
            new_name='_order',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='short_description',
            new_name='_short_description',
        ),
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='theme',
            new_name='_theme',
        ),
        migrations.RemoveField(
            model_name='buildingblockinstance',
            name='title',
        ),
        migrations.AddField(
            model_name='buildingblockinstance',
            name='_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
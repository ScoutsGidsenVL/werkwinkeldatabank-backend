# Generated by Django 3.1 on 2020-10-02 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0012_auto_20201002_0721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buildingblockinstance',
            old_name='_order',
            new_name='order',
        ),
    ]

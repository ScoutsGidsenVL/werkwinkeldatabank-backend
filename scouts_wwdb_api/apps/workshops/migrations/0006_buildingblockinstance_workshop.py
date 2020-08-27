# Generated by Django 3.1 on 2020-08-27 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0005_auto_20200826_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingblockinstance',
            name='workshop',
            field=models.ForeignKey(default='f2d0f11a-d8c7-4ddb-ad10-1ed72532baa8', on_delete=django.db.models.deletion.RESTRICT, related_name='building_blocks', to='workshops.workshop'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1 on 2020-09-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workshops", "0004_auto_20200917_0959"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingblockinstance",
            name="buildingblock_necessities",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="buildingblocktemplate",
            name="buildingblock_necessities",
            field=models.TextField(blank=True, null=True),
        ),
    ]

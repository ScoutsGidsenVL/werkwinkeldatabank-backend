# Generated by Django 3.1 on 2020-10-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workshops", "0011_auto_20201001_1126"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buildingblockinstance",
            name="_buildingblock_necessities",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="buildingblockinstance",
            name="_description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="buildingblockinstance",
            name="_title",
            field=models.CharField(blank=True, default="", max_length=200),
            preserve_default=False,
        ),
    ]

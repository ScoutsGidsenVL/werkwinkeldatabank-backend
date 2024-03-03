# Generated by Django 3.1 on 2020-09-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workshops", "0006_workshop_short_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingblockinstance",
            name="is_sensitive",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="buildingblocktemplate",
            name="is_sensitive",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="workshop",
            name="duration",
            field=models.DurationField(),
        ),
    ]

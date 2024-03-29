# Generated by Django 3.1.2 on 2020-10-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workshops", "0030_remove_workshop_theme"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingblocktemplate",
            name="status",
            field=models.CharField(
                choices=[
                    ("PRIVATE", "Privé"),
                    ("PUBLICATION_REQUESTED", "Publicatie aangevraagd"),
                    ("PUBLISHED", "Gepubliceerd"),
                ],
                default="PRIVATE",
                max_length=30,
            ),
        ),
    ]

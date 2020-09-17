# Generated by Django 3.1 on 2020-09-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workshops", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workshop",
            name="workshop_status_type",
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
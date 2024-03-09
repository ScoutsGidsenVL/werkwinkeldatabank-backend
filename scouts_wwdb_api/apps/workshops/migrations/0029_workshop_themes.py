# Generated by Django 3.1.2 on 2020-10-16 14:59

from django.db import migrations, models


def make_many_workshops(apps, schema_editor):
    Workshop = apps.get_model("workshops", "Workshop")

    for workshop in Workshop.objects.all():
        workshop.themes.add(workshop.theme)


class Migration(migrations.Migration):
    dependencies = [
        ("workshops", "0028_auto_20201015_2002"),
    ]

    operations = [
        migrations.AddField(
            model_name="workshop",
            name="themes",
            field=models.ManyToManyField(related_name="workshops", to="workshops.Theme"),
        ),
        migrations.RunPython(make_many_workshops),
    ]

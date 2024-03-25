# Generated by Django 3.1 on 2020-10-05 14:32

from datetime import timedelta

from django.db import migrations, models

from ..models.enums.building_block_type import BuildingBlockType


def add_empty_building_block_template(apps, schema_editor):
    # We can't import the BuildingBlockTemplate model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    BuildingBlockTemplate = apps.get_model("workshops", "BuildingBlockTemplate")
    template = BuildingBlockTemplate(
        title="Empty template",
        description="The empty building block template",
        duration=timedelta(hours=1),
        building_block_type=BuildingBlockType.THEMATIC,
        is_default_empty=True,
    )
    template.save()


class Migration(migrations.Migration):
    dependencies = [
        ("workshops", "0014_auto_20201005_1240"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="buildingblockinstance",
            options={"ordering": ["order"]},
        ),
        migrations.AddField(
            model_name="buildingblocktemplate",
            name="is_default_empty",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(add_empty_building_block_template),
    ]

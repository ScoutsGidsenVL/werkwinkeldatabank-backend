from datetime import timedelta
from ..models import BuildingBlockInstance, BuildingBlockTemplate, Workshop


def building_block_instance_create(
    *, title: str, description: str, duration: timedelta, template: BuildingBlockTemplate, workshop: Workshop
) -> BuildingBlockInstance:
    instance = BuildingBlockInstance(
        title=title, description=description, duration=duration, template=template, workshop=workshop
    )
    instance.full_clean()
    instance.save()

    return instance


def building_block_instance_update(*, existing_instance: BuildingBlockInstance, **fields) -> BuildingBlockInstance:
    existing_instance.title = fields.get("title", existing_instance.title)
    existing_instance.description = fields.get("description", existing_instance.description)
    existing_instance.duration = fields.get("duration", existing_instance.duration)
    existing_instance.template = fields.get("template", existing_instance.template)

    existing_instance.full_clean()
    existing_instance.save()

    return existing_instance

from datetime import timedelta
from ..models import BuildingBlockInstance, BuildingBlockTemplate, Workshop, Category, Theme


def building_block_instance_create(
    *,
    title: str = "",
    description: str = "",
    duration: timedelta = None,
    template: BuildingBlockTemplate,
    workshop: Workshop,
    short_description: str = "",
    category: Category = None,
    theme: Theme = None,
    order: int,
    building_block_necessities: str = "",
    linked_template_values: bool = False,
) -> BuildingBlockInstance:
    instance = BuildingBlockInstance(
        title=title,
        description=description,
        duration=duration,
        template=template,
        workshop=workshop,
        short_description=short_description,
        category=category,
        theme=theme,
        order=order,
        building_block_necessities=building_block_necessities,
        linked_template_values=linked_template_values,
    )
    instance.full_clean()
    instance.save()

    return instance


def building_block_instance_update(*, existing_instance: BuildingBlockInstance, **fields) -> BuildingBlockInstance:
    existing_instance.title = fields.get("title", existing_instance._title)
    existing_instance.description = fields.get("description", existing_instance._description)
    existing_instance.duration = fields.get("duration", existing_instance._duration)
    existing_instance.category = fields.get("category", existing_instance._category)
    existing_instance.short_description = fields.get("short_description", existing_instance._short_description)
    existing_instance.theme = fields.get("theme", existing_instance._theme)
    existing_instance.order = fields.get("order", existing_instance.order)
    existing_instance.building_block_necessities = fields.get(
        "building_block_necessities", existing_instance._building_block_necessities
    )
    existing_instance.linked_template_values = fields.get(
        "linked_template_values", existing_instance.linked_template_values
    )

    existing_instance.full_clean()
    existing_instance.save()

    return existing_instance

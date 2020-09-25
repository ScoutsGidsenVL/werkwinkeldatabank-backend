from datetime import timedelta
from ..models import BuildingBlockInstance, BuildingBlockTemplate, Workshop, Category, Theme


def building_block_instance_create(
    *,
    title: str,
    description: str,
    duration: timedelta,
    template: BuildingBlockTemplate,
    workshop: Workshop,
    short_description: str = "",
    category: Category = None,
    theme: Theme = None,
    order: int,
    buildingblock_necessities: str,
    is_sensitive: bool = False,
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
        buildingblock_necessities=buildingblock_necessities,
        is_sensitive=is_sensitive,
    )
    instance.full_clean()
    instance.save()

    return instance


def building_block_instance_update(*, existing_instance: BuildingBlockInstance, **fields) -> BuildingBlockInstance:
    existing_instance.title = fields.get("title", existing_instance.title)
    existing_instance.description = fields.get("description", existing_instance.description)
    existing_instance.duration = fields.get("duration", existing_instance.duration)
    existing_instance.category = fields.get("category", existing_instance.category)
    existing_instance.short_description = fields.get("short_description", existing_instance.short_description)
    existing_instance.template = fields.get("template", existing_instance.template)
    existing_instance.theme = fields.get("theme", existing_instance.theme)
    existing_instance.order = fields.get("order", existing_instance.order)
    existing_instance.buildingblock_necessities = fields.get(
        "buildingblock_necessities", existing_instance.buildingblock_necessities
    )
    existing_instance.is_sensitive = fields.get("is_sensitive", existing_instance.is_sensitive)

    existing_instance.full_clean()
    existing_instance.save()

    return existing_instance

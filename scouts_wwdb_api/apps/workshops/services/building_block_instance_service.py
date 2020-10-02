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
    buildingblock_necessities: str,
    is_sensitive: bool = False,
) -> BuildingBlockInstance:
    instance = BuildingBlockInstance(
        _title=title,
        _description=description,
        _duration=duration,
        template=template,
        workshop=workshop,
        _short_description=short_description,
        _category=category,
        _theme=theme,
        order=order,
        _buildingblock_necessities=buildingblock_necessities,
        _is_sensitive=is_sensitive,
    )
    instance.full_clean()
    instance.save()

    return instance


def building_block_instance_update(*, existing_instance: BuildingBlockInstance, **fields) -> BuildingBlockInstance:
    existing_instance._title = fields.get("title", existing_instance._title)
    existing_instance._description = fields.get("description", existing_instance._description)
    existing_instance._duration = fields.get("duration", existing_instance._duration)
    existing_instance._category = fields.get("category", existing_instance._category)
    existing_instance._short_description = fields.get("short_description", existing_instance._short_description)
    existing_instance.template = fields.get("template", existing_instance.template)
    existing_instance._theme = fields.get("theme", existing_instance._theme)
    existing_instance.order = fields.get("order", existing_instance.order)
    existing_instance._buildingblock_necessities = fields.get(
        "buildingblock_necessities", existing_instance._buildingblock_necessities
    )
    existing_instance._is_sensitive = fields.get("is_sensitive", existing_instance._is_sensitive)

    existing_instance.full_clean()
    existing_instance.save()

    return existing_instance

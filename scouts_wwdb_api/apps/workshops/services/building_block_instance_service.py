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

    existing_instance.full_clean()
    existing_instance.save()

    return existing_instance

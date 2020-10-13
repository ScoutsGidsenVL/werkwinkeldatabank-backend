from datetime import timedelta
from ..models import BuildingBlockTemplate, Category, Theme
from .history_service import history_create
from apps.base.services.disabled_field_service import update_is_disabled_field


def building_block_template_create(
    *,
    title: str,
    description: str,
    duration: timedelta,
    category: Category = None,
    building_block_type,
    short_description: str = "",
    theme: Theme = None,
    building_block_necessities: str = "",
    is_sensitive: bool = False,
    is_disabled: bool = False,
) -> BuildingBlockTemplate:
    template = BuildingBlockTemplate(
        title=title,
        description=description,
        duration=duration,
        category=category,
        building_block_type=building_block_type,
        short_description=short_description,
        theme=theme,
        building_block_necessities=building_block_necessities,
        is_sensitive=is_sensitive,
        is_disabled=is_disabled,
    )
    template.full_clean()
    template.save()

    return template


def building_block_template_update(*, existing_template: BuildingBlockTemplate, **fields) -> BuildingBlockTemplate:
    existing_template.title = fields.get("title", existing_template.title)
    existing_template.description = fields.get("description", existing_template.description)
    existing_template.duration = fields.get("duration", existing_template.duration)
    existing_template.category = fields.get("category", existing_template.category)
    existing_template.building_block_type = fields.get("building_block_type", existing_template.building_block_type)
    existing_template.short_description = fields.get("short_description", existing_template.short_description)
    existing_template.theme = fields.get("theme", existing_template.theme)
    existing_template.building_block_necessities = fields.get(
        "building_block_necessities", existing_template.building_block_necessities
    )
    existing_template.is_sensitive = fields.get("is_sensitive", existing_template.is_sensitive)
    update_is_disabled_field(instance=existing_template, **fields)

    existing_template.full_clean()
    existing_template.save()

    return existing_template


def building_block_template_add_history(*, data: dict, template: BuildingBlockTemplate):
    return history_create(data=data, building_block=template)

from ..models import Workshop, Theme
from django.shortcuts import get_object_or_404
from django.db import transaction
from .building_block_instance_service import building_block_instance_create, building_block_instance_update
from pprint import pprint

# Make atomic so database changes can be rolled back if error occurs
@transaction.atomic
def workshop_create(
    *,
    title: str,
    duration: str,
    theme: Theme,
    description: str,
    necessities: str,
    building_blocks: list,
    is_sensitive: bool = False,
) -> Workshop:
    workshop = Workshop(
        title=title,
        duration=duration,
        theme=theme,
        description=description,
        necessities=necessities,
        is_sensitive=is_sensitive,
    )
    workshop.save()

    for building_block_data in building_blocks:
        building_block = building_block_instance_create(**building_block_data, workshop=workshop)

    # We have to validate workshop after save because workshop needs to be saved before we can add building blocks to it
    # But because this is an atomic transaction if this fails now after save there will still not be any data in the database
    workshop.full_clean()
    return workshop


# Make atomic so database changes can be rolled back if error occurs
@transaction.atomic
def workshop_update(*, existing_workshop: Workshop, **fields) -> Workshop:
    existing_workshop.title = fields.get("title", existing_workshop.title)
    existing_workshop.description = fields.get("description", existing_workshop.description)
    existing_workshop.duration = fields.get("duration", existing_workshop.duration)
    existing_workshop.theme = fields.get("theme", existing_workshop.theme)
    existing_workshop.necessities = fields.get("necessities", existing_workshop.necessities)

    # Handle building blocks
    new_building_blocks_data = fields.get("building_blocks", None)
    if new_building_blocks_data:
        # Maps for id->instance and id->data item (if no id given just use index).
        instance_mapping = {block.id: block for block in existing_workshop.building_blocks.all()}
        data_mapping = {item.get("id", index): item for index, item in enumerate(new_building_blocks_data)}
        # Update existing and create new
        new_building_blocks = []
        for block_id, data in data_mapping.items():
            existing_block = instance_mapping.get(block_id, None)
            if existing_block:
                new_building_blocks.append(building_block_instance_update(existing_instance=existing_block, **data))
            else:
                new_building_blocks.append(building_block_instance_create(**data, workshop=existing_workshop))

        # Delete old
        for block_id, instance in instance_mapping.items():
            if block_id not in data_mapping:
                instance.delete()

    existing_workshop.full_clean()
    existing_workshop.save()

    return existing_workshop

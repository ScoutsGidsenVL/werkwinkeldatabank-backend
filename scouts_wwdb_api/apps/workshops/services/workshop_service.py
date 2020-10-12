from ..models import Workshop, Theme
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.base.services.disabled_field_service import update_is_disabled_field
from apps.wwdb_mails.services import send_template_mail
from .building_block_instance_service import building_block_instance_create, building_block_instance_update
from ..models.enums.workshop_status_type import WorkshopStatusType
from ..exceptions import InvalidWorkflowTransitionException


# Make atomic so database changes can be rolled back if error occurs
@transaction.atomic
def workshop_create(
    *,
    title: str,
    theme: Theme,
    description: str,
    building_blocks: list,
    approving_team=None,
    necessities: str = "",
    short_description: str = "",
    created_by: settings.AUTH_USER_MODEL,
    is_disabled: bool = False,
) -> Workshop:
    workshop = Workshop(
        title=title,
        theme=theme,
        description=description,
        necessities=necessities,
        short_description=short_description,
        created_by=created_by,
        approving_team=approving_team,
        is_disabled=is_disabled,
    )
    workshop.save()

    for index, building_block_data in enumerate(building_blocks):
        building_block = building_block_instance_create(**building_block_data, order=index, workshop=workshop)

    workshop.calculate_duration()

    # We have to validate workshop after save because workshop needs to be saved before we can add building blocks to it
    # But because this is an atomic transaction if this fails now after save there will still not be any data in the database
    workshop.full_clean()
    # save again to save duration
    workshop.save()
    return workshop


# Make atomic so database changes can be rolled back if error occurs
@transaction.atomic
def workshop_update(*, existing_workshop: Workshop, **fields) -> Workshop:
    existing_workshop.title = fields.get("title", existing_workshop.title)
    existing_workshop.description = fields.get("description", existing_workshop.description)
    existing_workshop.theme = fields.get("theme", existing_workshop.theme)
    existing_workshop.necessities = fields.get("necessities", existing_workshop.necessities)
    existing_workshop.short_description = fields.get("short_description", existing_workshop.short_description)
    existing_workshop.approving_team = fields.get("approving_team", existing_workshop.approving_team)
    update_is_disabled_field(instance=existing_workshop, **fields)

    # Handle building blocks
    new_building_blocks_data = fields.get("building_blocks", None)
    if new_building_blocks_data:
        # Maps for id->instance and id->data item (if no id given just use index).
        instance_mapping = {block.id: block for block in existing_workshop.building_blocks.all()}
        data_mapping = {item.get("id", index): item for index, item in enumerate(new_building_blocks_data)}
        # Update existing and create new
        new_building_blocks = []
        for index, (block_id, data) in enumerate(data_mapping.items()):
            existing_block = instance_mapping.get(block_id, None)
            if existing_block:
                new_building_blocks.append(
                    building_block_instance_update(existing_instance=existing_block, order=index, **data)
                )
            else:
                new_building_blocks.append(
                    building_block_instance_create(**data, order=index, workshop=existing_workshop)
                )

        # Delete old
        for block_id, instance in instance_mapping.items():
            if block_id not in data_mapping:
                instance.delete()

    existing_workshop.calculate_duration()
    existing_workshop.full_clean()
    existing_workshop.save()

    return existing_workshop


def workshop_request_publication(*, workshop: Workshop) -> Workshop:
    new_status = WorkshopStatusType.PUBLICATION_REQUESTED
    if not workshop.workshop_status_type == WorkshopStatusType.PRIVATE:
        raise InvalidWorkflowTransitionException(from_status=workshop.workshop_status_type, to_status=new_status)

    workshop.workshop_status_type = new_status
    try:
        workshop.full_clean()
    except ValidationError as error:
        raise InvalidWorkflowTransitionException(
            from_status=workshop.workshop_status_type, to_status=new_status, extra=str(error)
        )
    send_template_mail(template="workshop_publication_requested", workshop=workshop)
    workshop.save()
    return workshop


def workshop_publish(*, workshop: Workshop) -> Workshop:
    new_status = WorkshopStatusType.PUBLISHED
    if not workshop.workshop_status_type == WorkshopStatusType.PUBLICATION_REQUESTED:
        raise InvalidWorkflowTransitionException(from_status=workshop.workshop_status_type, to_status=new_status)

    workshop.workshop_status_type = new_status
    workshop.published_at = timezone.now()
    try:
        workshop.full_clean()
    except ValidationError as error:
        raise InvalidWorkflowTransitionException(
            from_status=workshop.workshop_status_type, to_status=new_status, extra=str(error)
        )
    send_template_mail(template="workshop_published", workshop=workshop)
    workshop.save()
    return workshop


def workshop_unpublish(*, workshop: Workshop) -> Workshop:
    new_status = WorkshopStatusType.PRIVATE
    if not workshop.workshop_status_type == WorkshopStatusType.PUBLISHED:
        raise InvalidWorkflowTransitionException(from_status=workshop.workshop_status_type, to_status=new_status)

    workshop.workshop_status_type = new_status
    workshop.published_at = None
    try:
        workshop.full_clean()
    except ValidationError as error:
        raise InvalidWorkflowTransitionException(
            from_status=workshop.workshop_status_type, to_status=new_status, extra=str(error)
        )
    workshop.save()
    return workshop

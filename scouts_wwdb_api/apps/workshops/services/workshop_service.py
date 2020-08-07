from ..models import Workshop
from ..models import Theme
from django.shortcuts import get_object_or_404
import uuid


def workshop_create(*, title: str, duration: str, theme: str, description: str, necessities: str) -> Workshop:
    workshop = Workshop(
        title=title, duration=duration, theme_id=theme, description=description, necessities=necessities
    )
    workshop.full_clean()
    workshop.save()

    return workshop


def workshop_update(*, existing_workshop: Workshop, **fields) -> Workshop:
    if fields:
        existing_workshop.title = fields.get("title", existing_workshop.title)
        existing_workshop.description = fields.get("description", existing_workshop.description)
        existing_workshop.duration = fields.get("duration", existing_workshop.duration)
        existing_workshop.theme = get_object_or_404(Theme.objects, pk=fields.get("theme", existing_workshop.theme))
        existing_workshop.necessities = fields.get("necessities", existing_workshop.necessities)

        return existing_workshop

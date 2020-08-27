from ..models import Workshop, Theme
from django.shortcuts import get_object_or_404
import uuid


def workshop_create(*, title: str, duration: str, theme: Theme, description: str, necessities: str) -> Workshop:
    workshop = Workshop(title=title, duration=duration, theme=theme, description=description, necessities=necessities)
    workshop.full_clean()
    workshop.save()

    return workshop


def workshop_update(*, existing_workshop: Workshop, **fields) -> Workshop:
    existing_workshop.title = fields.get("title", existing_workshop.title)
    existing_workshop.description = fields.get("description", existing_workshop.description)
    existing_workshop.duration = fields.get("duration", existing_workshop.duration)
    existing_workshop.theme_ = fields.get("theme", existing_workshop.theme)
    existing_workshop.necessities = fields.get("necessities", existing_workshop.necessities)

    existing_workshop.full_clean()
    existing_workshop.save()

    return existing_workshop

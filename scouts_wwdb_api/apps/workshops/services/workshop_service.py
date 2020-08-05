from ..models import Workshop
from ..models import Theme
from django.shortcuts import get_object_or_404
import uuid


def workshop_create(*, title: str, duration: str, theme: str, description: str, necessities: str) -> Workshop:
    theme_object = get_object_or_404(Theme.objects, pk=theme)
    workshop = Workshop(
        title=title, duration=duration, theme=theme_object, description=description, necessities=necessities
    )
    workshop.full_clean()
    workshop.save()

    return workshop

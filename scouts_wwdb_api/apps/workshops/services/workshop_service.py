from ..models import Workshop
from ..models import Theme
import uuid


def workshop_create(*, title: str, duration: str, theme: str, description: str, necessities: str) -> Workshop:
    workshop = Workshop(
        title=title, duration=duration, theme_id=theme, description=description, necessities=necessities
    )
    workshop.full_clean()
    workshop.save()

    return workshop

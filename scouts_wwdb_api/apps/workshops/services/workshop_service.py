from ..models import Workshop


def workshop_create(*, title: str, duration: str, description: str, necessities: str) -> Workshop:
    workshop = Workshop(title=title, duration=duration, description=description, necessities=necessities)
    workshop.full_clean()
    workshop.save()

    return workshop

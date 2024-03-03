from apps.base.services.disabled_field_service import update_is_disabled_field

from ..models import Theme


def theme_create(*, title: str, description: str = "", is_disabled: bool = False) -> Theme:
    theme = Theme(
        title=title,
        description=description,
        is_disabled=is_disabled,
    )
    theme.full_clean()
    theme.save()

    return theme


def theme_update(*, existing_theme: Theme, **fields) -> Theme:
    existing_theme.title = fields.get("title", existing_theme.title)
    existing_theme.description = fields.get("description", existing_theme.description)
    update_is_disabled_field(instance=existing_theme, **fields)

    existing_theme.full_clean()
    existing_theme.save()

    return existing_theme

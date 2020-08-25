from ..models import Theme


def theme_create(*, title: str, description: str) -> Theme:
    theme = Theme(title=title, description=description)
    theme.full_clean()
    theme.save()

    return theme


def theme_update(*, existing_theme: Theme, **fields) -> Theme:
    existing_theme.title = fields.get("title", existing_theme.title)
    existing_theme.description = fields.get("description", existing_theme.description)

    existing_theme.full_clean()
    existing_theme.save()

    return existing_theme

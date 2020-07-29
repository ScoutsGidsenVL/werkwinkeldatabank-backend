from ..models import Theme


def theme_create(*, title: str, description: str) -> Theme:
    theme = Theme(title=title, description=description)
    theme.full_clean()
    theme.save()

    return theme

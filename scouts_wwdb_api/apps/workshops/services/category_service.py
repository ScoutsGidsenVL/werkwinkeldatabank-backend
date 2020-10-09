from ..models import Category
from apps.base.services.disabled_field_service import update_is_disabled_field


def category_create(*, title: str, is_disabled: bool = False) -> Category:
    category = Category(
        title=title,
        is_disabled=is_disabled,
    )
    category.full_clean()
    category.save()

    return category


def category_update(*, existing_category: Category, **fields) -> Category:
    existing_category.title = fields.get("title", existing_category.title)
    update_is_disabled_field(instance=existing_category, **fields)

    existing_category.full_clean()
    existing_category.save()

    return existing_category

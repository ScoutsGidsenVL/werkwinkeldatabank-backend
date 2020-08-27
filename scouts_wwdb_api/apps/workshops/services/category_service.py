from ..models import Category


def category_create(*, title: str) -> Category:
    category = Category(title=title)
    category.full_clean()
    category.save()

    return category


def category_update(*, existing_category: Category, **fields) -> Category:
    existing_category.title = fields.get("title", existing_category.title)

    existing_category.full_clean()
    existing_category.save()

    return existing_category

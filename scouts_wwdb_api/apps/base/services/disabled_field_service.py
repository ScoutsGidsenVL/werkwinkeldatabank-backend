"""apps.base.services.disabled_field_service."""


def update_is_disabled_field(*, instance, **fields):
    instance.is_disabled = fields.get("is_disabled", instance.is_disabled)

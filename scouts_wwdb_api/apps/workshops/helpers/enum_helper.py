"""apps.workshops.helpers.enum_helper."""


def parse_choice_to_tuple(choice) -> tuple:
    return (choice.value, choice.label)

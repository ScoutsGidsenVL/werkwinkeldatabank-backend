"""apps.workshops.exceptions."""


class InvalidWorkflowTransitionException(Exception):
    def __init__(self, from_status: str, to_status: str, extra: str = "Can't transition between statuses"):
        message = f"Invalid workflow transition from status {from_status} to status {to_status}"
        if extra:
            message += f": {extra}"
        return super().__init__(message)

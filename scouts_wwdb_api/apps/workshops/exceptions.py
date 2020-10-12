class InvalidWorkflowTransitionException(Exception):
    def __init__(self, from_status: str, to_status: str, extra: str = "Can't transition between statuses"):
        message = "Invalid workflow transition from status %s to status %s" % (
            from_status,
            to_status,
        )
        if extra:
            message += ": " + extra
        return super().__init__(message)

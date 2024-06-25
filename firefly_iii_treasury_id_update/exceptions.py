class WebsocketConnectionError(Exception):
    """Raised when problem happend during recv and send to websockets"""

    pass


class ConnectionClosedError(Exception):
    """Internal use only, raised when problem whappened during recv to websockets while in retrieving gold-rate data"""

    pass


class MissingArguments(Exception):
    pass

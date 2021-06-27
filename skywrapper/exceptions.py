class SkywrapperException(Exception):
    """
    Used as the base exception for errors that are specific to this package.

    This exception may be caught to handle most exceptions thrown from this library.
    """
    pass


class BaseMojangException(SkywrapperException):
    """
    Used as the base error for all Mojang API related errors.
    """
    pass


class HTTPException(SkywrapperException):
    """
    Thrown when an HTTP operation fails. Also a base class for other HTTP related errors.

    You should catch more specific errors instead of catching this one in most cases.

    :cvar response: :class:`requests.Response` or :class:`aiohttp.Response`
    """
    response = None
    pass

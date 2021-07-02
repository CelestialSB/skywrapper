# exceptions.py: Custom exceptions
# Copyright (C) 2021-present kcomain, seazyns and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Union

from requests import Response
try:
    from aiohttp import ClientResponse
except ImportError:
    ClientResponse = None


class SkywrapperException(Exception):
    """
    Used as the base exception for errors that are specific to this package.

    This exception may be caught to handle most exceptions thrown from this library.
    """
    pass


class HTTPException(SkywrapperException):
    """
    Thrown when an HTTP operation fails. Also a base class for other HTTP related errors.

    You should catch more specific errors instead of catching this one when suitable.

    :ivar response: :class:`requests.Response` or :class:`aiohttp.ClientResponse`
    :ivar status_code: HTTP Status code
    :ivar response_message: The response body returned
    """
    def __init__(self, response: Union[Response, ClientResponse],
                 status_code: int,
                 response_message: Union[dict, str]
                 ):
        self.response = response
        super().__init__()


class MojangException(HTTPException):
    """
    Used as the base error for most Mojang API related errors.

    Subclass of :exc:`HTTPException`
    """
    pass


class InvalidType(SkywrapperException):
    """
    Raises when an incompatible type is used.
    """
    pass


class NotFoundException(HTTPException):
    """
    Thrown when an HTTP request returns a 404 status code.

    Subclass of :exc:`HTTPException`
    """
    pass


class UnauthorizedException(HTTPException):
    """
    Thrown when an HTTP request returns a 403 status code

    Subclass of :exc:`HTTPException`
    """

# http.py: http helper methods
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

import sys
from typing import Union
# from enum import Enum

import requests

from . import __version__


class MojangRoute:
    """
    :param reqtype: Request type, can be one of ``["api", "session"]``
    :param endpoint: API Endpoint to send request to

    :ivar method: HTTP Method to use
    :cvar API_ROUTE: base api url
    :cvar SESSION_ROUTE: base session server api url
    """
    API_ROUTE = "https://api.mojang.com"
    SESSION_ROUTE = "https://sessionserver.mojang.com"

    def __init__(self, method: str, reqtype: str, endpoint: str):
        self.method = method
        self._reqtype = reqtype.lower()
        self._endpoint = endpoint
        pass

    @property
    def url(self) -> str:
        """
        Full URL without any data

        :return: Full API request URL
        """
        return (self.__class__.API_ROUTE if self._reqtype == "api" else self.__class__.SESSION_ROUTE) + self._endpoint


class HypixelRoute:
    """
    :param endpoint: API Endpoint to send request to

    :ivar method: HTTP Method to use
    :cvar BASE: base api url
    """
    BASE = "https://api.hypixel.net"

    def __init__(self, method: str, endpoint: str):
        """
        うおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおお
        """
        self.method = method
        self._endpoint = endpoint
        pass

    @property
    def url(self) -> str:
        """
        Full URL without any data

        :return: Full API request URL
        """
        return self.__class__.BASE + self._endpoint


class HTTPClient:
    """
    Responsible for starting the great robot uprise and the destruction of humanity.

    Also responsible for communication of this library.

    I don't know why I added this class, though it may prove useful when adding async support.

    :param useragent: User-Agent string to use, auto generated if not provided.
    """

    def __init__(self, useragent: str = None):
        """
        おはよう
        """
        self.useragent = useragent if useragent else \
            "Skywrapper (https://github.com/CelestialSB/skywrapper {lib_version}) " \
            "Python/{py_ver[0]}{py_ver[1]}{py_ver[2]} requests/{req_ver}".format(lib_version=__version__,
                                                                                 py_ver=sys.version_info,
                                                                                 req_ver=requests.__version__)

    def request(self, route: Union[MojangRoute, HypixelRoute], **kwargs):
        """
        Send an HTTP request

        :param route: one of :class:`~.MojangRoute` or :class:`~.HypixelRoute`
            route.url
        :keyword kwargs: keyword arguments to pass to :func:`requests.request`
        :return:
        """
        headers = kwargs.get('headers')
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.useragent

        kwargs['headers'] = headers
        result = requests.request(route.method, route.url, **kwargs)

        # TODO: add status code checks and throw exceptions when necessary
        return result

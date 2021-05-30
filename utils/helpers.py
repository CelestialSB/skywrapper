from aiohttp import ClientSession  # formatting conv


async def get_json(url: str, **kwargs):
    """
    Sends a GET request and return the JSON body asynchronously

    :param url: The URL
    :param kwargs: Other keyword arguments to pass to aiohttp.ClientSession.get(),
        see https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request
    """
    async with ClientSession() as session:
        async with session.get(url, **kwargs) as res:
            return await res.json()

# import requests
import logging

from constants.bot_config import API_KEY
from utils.errors import InvalidIGN, SkyblockAPIError
from utils.helpers import get_json

logger = logging.getLogger("api")


# Get Mojang Data
async def get_mojang_data(name: str = None, uuid: str = None):
    """
    :param name: Player name (IGN)
    :param uuid: Player UUID
    :returns: tuple(str, str)
    :rtype: tuple[str, str]

    [Returns type: string, string] Gets UUID and Minecraft IGN
    """
    try:
        if name is not None:
            logger.info(f"GET https://api.mojang.com/users/profiles/minecraft/{name}")
            mojang_data = await get_json(f"https://api.mojang.com/users/profiles/minecraft/{name}")
            return mojang_data["id"], mojang_data["name"]
        if uuid is not None:
            logger.info(f"GET https://api.mojang.com/user/profiles/{uuid}/names")
            mojang_data = await get_json(f"https://api.mojang.com/user/profiles/{uuid}/names")
            return uuid, mojang_data[-1]["name"]
    # except:  # avoid using bare except
    except Exception as e:
        raise InvalidIGN(e)


# Skyblock Data
async def get_skyblock_data(uuid: str):
    """
    :param uuid: Player UUID
    :returns: Skyblock data
    :rtype: dict

    [Returns type: dict] Gets skyblock data
    """
    try:
        logger.info(f"GET https://api.hypixel.net/skyblock/profiles?key=API_KEY&uuid={uuid}")
        skyblock_data = await get_json(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}")
        return skyblock_data
    except Exception as e:
        raise SkyblockAPIError(e)


# Hypixel Data
async def get_hypixel_data(uuid: str) -> dict:
    """
    :param uuid: Player UUID
    :returns: hypixel data
    :rtype: dict
    [Returns type: dict] Gets hypixel data
    """
    logger.info(f"GET https://api.hypixel.net/player?key=API_KEY&uuid={uuid}")
    hypixel_data = await get_json(f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}")

    if "socialMedia" in hypixel_data["player"] and "DISCORD" in hypixel_data["player"]["socialMedia"]["links"]:
        discord = hypixel_data["player"]["socialMedia"]["links"]["DISCORD"]  # .lower()
    else:
        discord = None
    return hypixel_data, discord


# Bazaar Data
async def get_bazaar_data():
    """
    :returns: bazaar data
    :rtype: dict

    [Returns type: dict] Gets bazaar data
    """
    logger.info("GET https://sky.lea.moe/api/bazaar")
    bazaar_data = await get_json("https://sky.lea.moe/api/bazaar")
    return bazaar_data


# Auction Data
async def get_auction_data(uuid: str):
    """
    :param uuid: Player UUID
    :rtype: dict
    :returns: Specified player's auction data

    [Returns type: dict] Gets player auction data
    """
    logger.info(f"GET https://api.hypixel.net/skyblock/auction?key=API_KEY&player={uuid}")
    auction_data = await get_json(f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&player={uuid}")
    return auction_data


async def get_leaderboard_data(leaderboard_id, page=1, name=None):
    """
    Gets leaderboard data from sky.lea.moe

    :param leaderboard_id: Leaderboard ID
    :param page: Page number for pagination
    :param name: Find a player
    :return: Leaderboard data
    :rtype: dict
    """
    if name is None:
        logger.info(f"GET https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?page={page}")
        leaderboard_data = await get_json(f"https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?page={page}")
    else:
        logger.info(f"GET https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?find={name}")
        try:
            leaderboard_data = await get_json(f"https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?find={name}")
        except Exception as e:
            raise InvalidIGN(e)
    return leaderboard_data

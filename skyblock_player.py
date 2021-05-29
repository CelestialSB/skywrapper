import api_data
import profile_info
import skyblock_data


class SkyblockPlayer:
    def __init__(self,
                 mc_name=None,
                 uuid=None,
                 profile_name=None, *,
                 get_hypixel_data=False,
                 get_bazaar_data=False,
                 get_auction_data=False) -> None:
        """
        Represents a Skyblock Player

        :param mc_name: The player's in game name
        :param uuid: The player's UUID
        :param profile_name: The player's skyblock profile name
        :keyword get_bazaar_data: whether or not to get bazaar data
        :keyword get_hypixel_data: whether or not to get hypixel data
        :keyword get_auction_data: whether or not to get auction data
        """
        self._ign = mc_name
        self._uuid = uuid
        self._profilename = profile_name
        self._getdata = {
            'hypixel': get_hypixel_data,
            'bazaar': get_bazaar_data,
            'auction': get_auction_data,
        }

        # Data / Info
        self.uuid, self.mc_name = ('', '')
        self.skyblock_data = {}
        self.hypixel_data, self.linked_discord = "Not requested", "None"  # {}, ""
        self.bazaar_data = "Not requested"
        self.auction_data = 'Not requested'

        # Profiles
        self.profiles = []
        self.latest_profile_name, self.latest_profile_index = profile_info.get_latest_profile(self.skyblock_data, self.uuid)
        self.profile_name, self.profile_index = profile_info.get_profile_info(self.skyblock_data, profile_name, self.profiles, self.latest_profile_name, self.latest_profile_index)

        # Extra
        self.purse, self.bank = skyblock_data.get_money(self.skyblock_data, self.profile_index, self.uuid)
        self.rock_milestone, self.dolphin_milestone, self.next_rock_milestone, self.next_dolphin_milestone, self.rock_rarity, self.dolphin_rarity = skyblock_data.get_pet_milestones(self.skyblock_data, self.profile_index, self.uuid)
        self.currently_upgrading, self.coop_upgrades = skyblock_data.get_community_upgrades(self.skyblock_data, self.profile_index)
        self.jacob_medals, self.jacob_upgrades, self.jacob_info = skyblock_data.get_jacob_data(self.skyblock_data, self.profile_index, self.uuid)
        self.secrets, self.dungeon_class, self.cata_xp, self.cata_level, self.class_xp, self.dungeon_floor_info = skyblock_data.get_dungeons_data(get_hypixel_data, self.skyblock_data, self.hypixel_data, self.profile_index, self.uuid)
        self.slayer_info = skyblock_data.get_slayer_data(self.skyblock_data, self.profile_index, self.uuid)
        self.skills_info, self.total_xp = skyblock_data.get_skills_data(self.skyblock_data, self.profile_index, self.uuid)
        self.bazaar_info = {}

        # Inventory Data
        # self.inventory = inventory_data.get_inventory_data(self.skyblock_data, self.profile_index, self.uuid)

    async def load_data(self) -> None:
        """
        Loads data from the API asynchronously

        :return: Nothing
        """
        # Raw API data
        self.uuid, self.mc_name = await api_data.get_mojang_data(self._ign, self._uuid)
        self.skyblock_data = await api_data.get_skyblock_data(self.uuid)

        # Information depending on skyblock data
        self.profiles = profile_info.get_profiles(self.skyblock_data)
        self.purse, self.bank = skyblock_data.get_money(self.skyblock_data)

        # Information depending on hypixel data
        # -> profiles
        if self._getdata['hypixel']:
            self.hypixel_data = await api_data.get_hypixel_data(self.uuid)
            self.linked_discord = self.hypixel_data['player']['socialMedia']['links']['DISCORD']

        # Information depending on bazaar data
        if self._getdata['bazaar']:
            self.bazaar_data = await api_data.get_bazaar_data()
            self.bazaar_info = skyblock_data.get_bazaar_info(self.bazaar_data)

        # Information depending on auction data
        if self._getdata['auction']:
            self.auction_data = await api_data.get_auction_data(self.uuid)

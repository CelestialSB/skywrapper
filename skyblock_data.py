# import math
from constants.skyblock import *


def get_money(skyblock_data, profile_index, uuid):
    """
    [Returns type: int (purse), int (bank)] Gets purse coins & bank coins values based on profile name
    """
    purse_amount = round(skyblock_data['profiles'][profile_index]['members'][uuid].get('coin_purse', 0))
    bank_amount = (
        round(skyblock_data['profiles'][profile_index]['banking']['balance']) if 'banking' in skyblock_data['profiles'][
            profile_index] else 'Bank API Disabled')
    return purse_amount, bank_amount


def get_pet_milestones(skyblock_data, profile_index, uuid):
    """
    [Returns type: int (rock), int (dolphin)] Gets pet milestones for dolphin and rock
    """
    rock_milestone = round(
        skyblock_data['profiles'][profile_index]['members'][uuid]['stats'].get('pet_milestone_ores_mined', 0))
    dolphin_milestone = round(
        skyblock_data['profiles'][profile_index]['members'][uuid]['stats'].get('pet_milestone_sea_creatures_killed', 0))
    next_rock_milestone = (
        [value for key, value in MILESTONE_TABLE['rock'].items() if value > rock_milestone][0] if len(
            [value for key, value in MILESTONE_TABLE['rock'].items() if value > rock_milestone]) != 0 else 'Complete')
    next_dolphin_milestone = (
        [value for key, value in MILESTONE_TABLE['dolphin'].items() if value > dolphin_milestone][0] if len(
            [value for key, value in MILESTONE_TABLE['dolphin'].items() if
             value > dolphin_milestone]) != 0 else 'Complete')
    rock_rarity = [key for key, value in MILESTONE_TABLE['rock'].items() if rock_milestone >= value][-1]
    dolphin_rarity = [key for key, value in MILESTONE_TABLE['dolphin'].items() if dolphin_milestone >= value][-1]
    return rock_milestone, dolphin_milestone, next_rock_milestone, next_dolphin_milestone, rock_rarity, dolphin_rarity


def get_community_upgrades(skyblock_data, profile_index):
    """
    [Returns type: string (currently upgrading), dict (coop upgrades)] Gets community upgrades and currently upgrading
    """
    upgrade_data = skyblock_data['profiles'][profile_index].get('community_upgrades', {})
    currently_upgrading = (upgrade_data['currently_upgrading'].get('upgrade', None).replace('_',
                                                                                            ' ').title() if 'currently_upgrading' in upgrade_data and
                                                                                                            upgrade_data[
                                                                                                                'currently_upgrading'] is not None else None)
    coop_upgrades = {upgrade_name: {
        'name': upgrade_value['name'],
        'level': 0,
        'max_level': upgrade_value['max_level']
    } for upgrade_name, upgrade_value in COOP_UPGRADES_TEMPLATE.items()}

    for upgrade in upgrade_data.get('upgrade_states', {}):
        coop_upgrades[upgrade['upgrade']]['level'] += 1
    return currently_upgrading, coop_upgrades


def get_jacob_data(skyblock_data, profile_index, uuid):
    """
    [Returns type: dict (medals), dict (upgrades), dict (unique gold & highscore)] Gets jacob's event data
    """
    jacobs_data = skyblock_data['profiles'][profile_index]['members'][uuid].get('jacob2', {})
    jacobs_medals = {medal_name: (
        jacobs_data['medals_inv'][medal_name] if 'medals_inv' in jacobs_data and medal_name in jacobs_data[
            'medals_inv'] else medal_value) for medal_name, medal_value in JACOBS_MEDALS_TEMPLATE.items()}
    jacobs_upgrades = {upgrade_name: {
        'level': (
            jacobs_data['perks'][upgrade_name] if 'perks' in jacobs_data and upgrade_name in jacobs_data['perks'] else
            JACOBS_UPGRADES_TEMPLATE[upgrade_name]['level']),
        'max_level': JACOBS_UPGRADES_TEMPLATE[upgrade_name]['max_level']
    } for upgrade_name in JACOBS_UPGRADES_TEMPLATE.keys()}
    jacobs_info = {item_id: {
        'name': item_value['name'],
        'gold_status': (True if ('unique_golds2' in jacobs_data and item_id in jacobs_data['unique_golds2']) or (
                    'unique_golds2' in jacobs_data and item_id == 'INK_SACK' and 'INK_SACK:3' in jacobs_data[
                'unique_golds2']) else False),
        'highscore': max(
            [event_value['collected'] for event_name, event_value in jacobs_data.get('contests', {}).items() if
             item_id in event_name], default=0)
    } for item_id, item_value in JACOBS_INFO_TEMPLATE.items()}
    return jacobs_medals, jacobs_upgrades, jacobs_info


def get_dungeons_data(get_hypixel_data, skyblock_data, hypixel_data, profile_index, uuid):
    """
    [Returns type: int (secrets), string (dungeon class), int (cata xp), int (cata level), dict (class xp), dict (floor info)] Gets catacombs data
    """
    dungeon_data = skyblock_data['profiles'][profile_index]['members'][uuid].get('dungeons', {})
    secrets = (hypixel_data['player']['achievements'].get('skyblock_treasure_hunter', 0) if get_hypixel_data else 0)
    dungeon_class = dungeon_data.get('selected_dungeon_class', 'None').capitalize()
    cata_xp = (
        dungeon_data['dungeon_types']['catacombs']['experience'] if 'dungeon_types' in dungeon_data and 'experience' in
                                                                    dungeon_data['dungeon_types']['catacombs'] else 0)
    cata_level = [key for key, value in DUNGEON_XP_TABLE.items() if cata_xp >= value][-1]
    class_xp = {class_name: (round(dungeon_data['player_classes'][class_name][
                                       'experience']) if 'player_classes' in dungeon_data and 'experience' in
                                                         dungeon_data['player_classes'][class_name] else 0) for
                class_name in DUNGEON_CLASS_XP_TEMPLATE.keys()}
    dungeon_floor_info = {key: {
        'name': value['name'],
        'best_score': (dungeon_data['dungeon_types']['catacombs']['best_score'][
                           key] if 'dungeon_types' in dungeon_data and 'best_score' in dungeon_data['dungeon_types'][
            'catacombs'] and key in dungeon_data['dungeon_types']['catacombs']['best_score'] else 0),
        'fastest_time_s': (dungeon_data['dungeon_types']['catacombs']['fastest_time_s'][
                               key] if 'dungeon_types' in dungeon_data and 'fastest_time_s' in
                                       dungeon_data['dungeon_types']['catacombs'] and key in
                                       dungeon_data['dungeon_types']['catacombs']['fastest_time_s'] else 0),
        'fastest_time_s_plus': (dungeon_data['dungeon_types']['catacombs']['fastest_time_s_plus'][
                                    key] if 'dungeon_types' in dungeon_data and 'fastest_time_s_plus' in
                                            dungeon_data['dungeon_types']['catacombs'] and key in
                                            dungeon_data['dungeon_types']['catacombs']['fastest_time_s_plus'] else 0),
        'completions': (dungeon_data['dungeon_types']['catacombs']['tier_completions'][
                            key] if 'dungeon_types' in dungeon_data and 'tier_completions' in
                                    dungeon_data['dungeon_types']['catacombs'] and key in
                                    dungeon_data['dungeon_types']['catacombs']['tier_completions'] else 0)
    } for key, value in DUNGEON_FLOOR_INFO_TEMPLATE.items()}
    return secrets, dungeon_class, cata_xp, cata_level, class_xp, dungeon_floor_info


def get_slayer_data(skyblock_data, profile_index, uuid):
    """
    [Returns type: dict (slayer info)] Gets slayer data
    """
    slayer_data = skyblock_data['profiles'][profile_index]['members'][uuid].get('slayer_bosses', {})
    slayer_info = {key: {
        'name': value['name'],
        'xp': slayer_data[key].get('xp', 0),
        'level': ([template_key for template_key, template_value in SLAYER_LEVEL[key].items() if
                   slayer_data[key].get('xp', 0) >= template_value])[-1]
    } for key, value in SLAYER_TEMPLATE.items()}
    return slayer_info


def get_skills_data(skyblock_data, profile_index, uuid):
    """
    [Returns type: dict (skills info)] Gets skills data
    """
    skills_data = skyblock_data['profiles'][profile_index]['members'][uuid]
    skills_info = {key: {
        'xp': (skills_data[key] if key in skills_data else 0),
        'name': key.split('_')[2].capitalize()
    } for key, value in SKILLS_TEMPLATE.items()}
    total_xp = 0
    for skill_name, skill_value in skills_info.items():
        total_xp += skill_value['xp']
    return skills_info, total_xp


def get_bazaar_info(bazaar_data: dict):
    bazaar_info = {}
    for item in bazaar_data:
        bazaar_info[item['name']] = {
            'id': item['id'],
            'instant_buy': item['buyPrice'],
            'instant_sell': item['sellPrice']
        }
    # bazaar_info = {
    #     item['name']: {
    #         'id': item['id'],
    #         'instant_buy': item['buyPrice'],
    #         'instant_sell': item['sellPrice']
    #     } for item in bazaar_data}  # readability
    return bazaar_info

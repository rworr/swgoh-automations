import json
import os
from enum import Enum

import requests

from comlink.StatDefinitions import STAT_DEFINITIONS


class Metadata:
    def __init__(self, metadata_response: dict):
        self.data_version = metadata_response["latestGamedataVersion"]
        self.localization_version = metadata_response["latestLocalizationBundleVersion"]


class Localization:
    _TARGET_LANG = 'Loc_ENG_US.txt'
    _ENTRY_SEP = '|'
    _COMMENT = '#'

    def __init__(self, comlink_metadata: dict[str, str]):
        self.entries = {}
        for line in comlink_metadata[Localization._TARGET_LANG].splitlines():
            if Localization._COMMENT != line[0] and Localization._ENTRY_SEP in line:
                key, val = line.split(Localization._ENTRY_SEP)
                self.entries[key] = val

    def get(self, key: str) -> str:
        return self.entries[key]


class Data:
    _COMBATTYPE_CHAR = 1
    _COMBATTYPE_SHIP = 2

    def __init__(self, data: dict, localization: Localization):
        # sort units by id `ZORIIBLISS_V2:SEVEN_STAR` which matches with player->unit->definitionId
        self.characters = {}
        for unit in data['units']:
            if unit['combatType'] == Data._COMBATTYPE_CHAR:
                self.characters[unit['id']] = localization.get(unit['nameKey'])
        # self.statMods = data['statMod']
        # self.categories = data['category']
        # self.abilities = data['abliity']


class ModSet(Enum):
    HEALTH = 1
    OFFENSE = 2
    DEFENSE = 3
    SPEED = 4
    CRITICAL_CHANCE = 5
    CRITICAL_DAMAGE = 6
    POTENCY = 7
    TENACITY = 8


class ModSlot(Enum):
    SQUARE = 1
    ARROW = 2
    DIAMOND = 3
    TRIANGLE = 4
    CIRCLE = 5
    CROSS = 6


class ModTier(Enum):
    A = 5
    B = 4
    C = 3
    D = 2
    E = 1


class ModStat:
    def __init__(self, stat_data: dict):
        self.statId = stat_data['stat']['unitStatId']
        self.name = STAT_DEFINITIONS[self.statId]['detailedName']
        self.isDecimal = STAT_DEFINITIONS[self.statId]['isDecimal']
        if self.isDecimal:
            self.displayValue = float(stat_data['stat']['unscaledDecimalValue']) / 1000000
        else:
            self.displayValue = int(stat_data['stat']['unscaledDecimalValue']) // 100000000
        self.statRolls = [int(r) for r in stat_data['unscaledRollValue']]
        self.statRollMin = int(stat_data['statRollerBoundsMin'])
        self.statRollMax = int(stat_data['statRollerBoundsMax'])


class Mod:
    def __init__(self, mod_data: dict):
        self.definition_id = int(mod_data["definitionId"])
        self.set = ModSet(self.definition_id // 100)
        self.slot = ModSlot(self.definition_id % 10)
        self.rarity = (self.definition_id // 10) % 10
        self.level = mod_data["level"]
        self.tier = ModTier(mod_data["tier"])
        self.rerolled_count = mod_data["rerolledCount"]
        self.primary_stat = ModStat(mod_data["primaryStat"])
        self.primary = self.primary_stat.name
        self.secondaries = [ModStat(stat) for stat in mod_data["secondaryStat"]]


class RosterUnit:
    def __init__(self, unit_data: dict, game_data: Data):
        self.definition_id = unit_data["definitionId"]
        self.name = game_data.characters[self.definition_id]
        self.current_rarity = unit_data["currentRarity"]
        self.current_level = unit_data["currentLevel"]
        self.current_tier = unit_data["currentTier"]
        self.relic = int(unit_data["relic"]["currentTier"]) - 2 if unit_data["relic"]["currentTier"] >= 2 else None
        self.mods = [Mod(payload) for payload in unit_data["equippedStatMod"]]


class Player:
    def __init__(self, player_data: dict, game_data: Data):
        self.name = player_data['name']
        self.ally_code = player_data['allyCode']
        self.player_id = player_data['playerId']
        self.guild_id = player_data['guildId']

        self.roster = []
        for unit_data in player_data['rosterUnit']:
            if unit_data['definitionId'] in game_data.characters:
                self.roster.append(RosterUnit(unit_data, game_data))


class Guild:
    def __init__(self, guild_data: dict):
        self.name = guild_data["guild"]["profile"]["name"]
        self.guild_id = guild_data["guild"]["profile"]["id"]
        self.player_ids = [member["playerId"] for member in guild_data["guild"]["member"]]


class Comlink:
    """
    TODO docstring, generics?
    """

    def __init__(self, uri=None):
        self.uri = uri if uri else os.getenv("COMLINK_URI")
        self.metadata = None
        self.localization = None
        self.data = None
        self._warm()

    def _warm(self):
        self.get_metadata()
        self.get_localization()
        self.get_data()
        print("Comlink ready!")

    def get_metadata(self) -> Metadata:
        if not self.metadata:
            print("Fetching game metadata...")
            payload = {"payload": {}}
            response = self._comlink_post(path="metadata", data=payload)
            self.metadata = Metadata(response)
        return self.metadata

    def get_localization(self) -> Localization:
        if not self.localization:
            print("Fetching localization data...")
            payload = {
                "unzip": True,
                "payload": {
                    "id": self.get_metadata().localization_version
                },
            }
            response = self._comlink_post(path="localization", data=payload)
            self.localization = Localization(response)
        return self.localization

    def get_data(self) -> Data:
        if not self.data:
            print("Fetching game data...")
            data_payload = {
                "payload": {
                    "version": self.get_metadata().data_version,
                    "includePveUnits": False,
                }
            }
            response = self._comlink_post(path="data", data=data_payload)
            self.data = Data(response, self.get_localization())
        return self.data

    def get_player_by_ally_code(self, ally_code: int) -> Player:
        print(f"Fetching information for player {ally_code}...")
        player_payload = {
            "payload": {
                "allyCode": str(ally_code)
            }
        }
        response = self._comlink_post(path="player", data=player_payload)
        return Player(player_data=response, game_data=self.get_data())

    def get_player_by_id(self, player_id: str) -> Player:
        print(f"Fetching information for player {player_id}...")
        player_payload = {
            "payload": {
                "playerId": player_id
            }
        }
        response = self._comlink_post(path="player", data=player_payload)
        return Player(player_data=response, game_data=self.get_data())

    def get_guild(self, guild_id: str) -> Guild:
        print(f"Fetching information for guild {guild_id}...")
        guild_payload = {
            "payload": {
                "guildId": guild_id
            }
        }
        response = self._comlink_post(path="guild", data=guild_payload)
        return Guild(guild_data=response)

    def _comlink_post(self, path: str, data: dict) -> dict:
        response = requests.post(
            url=os.path.join(self.uri, path),
            headers={"Content-Type": "application/json"},
            data=_comlink_dumps(data),
        )
        return response.json()


COMLINK = None


def get_comlink() -> Comlink:
    global COMLINK
    if COMLINK is None:
        # TODO: skip starting comlink if already running -> use docker SDK
        # run(["./comlink-start.sh"])
        COMLINK = Comlink()
    return COMLINK


def stop_comlink():
    # TODO: skip starting comlink if already running -> use docker SDK
    # run(["./comlink-stop.sh"])
    pass


def _comlink_dumps(obj: dict) -> str:
    return json.dumps(obj)

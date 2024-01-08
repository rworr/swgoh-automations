from comlink.RosterUnit import RosterUnit


class Player:
    def __init__(self, comlink_payload: dict):
        self.name = comlink_payload['name']
        self.level = comlink_payload['level']
        self.ally_code = comlink_payload['allyCode']
        self.player_id = comlink_payload['playerId']
        self.guild_id = comlink_payload['guildId']
        self.guild_name = comlink_payload['guildName']

        self.roster = [RosterUnit(payload) for payload in comlink_payload['rosterUnit']]

        # rosterUnit
        # TODO: datacrons? Load game data to get string resources?


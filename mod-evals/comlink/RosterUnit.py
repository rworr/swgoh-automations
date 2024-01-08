from comlink.Mod import Mod


class RosterUnit:
    def __init__(self, comlink_payload: dict):
        self.id = comlink_payload["id"]
        self.definition_id = comlink_payload["definitionId"]
        self.current_rarity = comlink_payload["currentRarity"]
        self.current_level = comlink_payload["currentLevel"]
        self.current_tier = comlink_payload["currentTier"]
        self.relic = comlink_payload["relic"]["currentTier"]

        self.mods = [Mod(payload) for payload in comlink_payload["equippedStatMod"]]
        # equipment
        # skills
        # stats

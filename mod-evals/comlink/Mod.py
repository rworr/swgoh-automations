class Mod:
    def __init__(self, comlink_data: dict):
        self.id = comlink_data["id"]
        self.definition_id = comlink_data["definitionId"]
        self.level = comlink_data["level"]
        self.tier = comlink_data["tier"]
        self.rerolled_count = comlink_data["rerolledCount"]


        self.primary_stat = comlink_data["primaryStat"] #TODO parse out
        self.secondary_stats =

        """
            "primaryStat": {
            "roll": [],
            "unscaledRollValue": [],
            "stat": {
                "unitStatId": 48,
                "statValueDecimal": "588",
                "unscaledDecimalValue": "5880000",
                "uiDisplayOverrideValue": "-1",
                "scalar": "0"
            },
            "statRolls": 0,
            "statRollerBoundsMin": "0",
            "statRollerBoundsMax": "0"
        },
        """

        """
        {
                    "secondaryStat": [
                        {
                            "roll": [
                                "0.17227"
                            ],
                            "unscaledRollValue": [
                                "1938"
                            ],
                            "stat": {
                                "unitStatId": 53,
                                "statValueDecimal": "193",
                                "unscaledDecimalValue": "1938000",
                                "uiDisplayOverrideValue": "-1",
                                "scalar": "0"
                            },
                            "statRolls": 1,
                            "statRollerBoundsMin": "1125",
                            "statRollerBoundsMax": "2250"
                        },
                        {
                            "roll": [
                                "0.12345",
                                "0.11920"
                            ],
                            "unscaledRollValue": [
                                "370350",
                                "357600"
                            ],
                            "stat": {
                                "unitStatId": 5,
                                "statValueDecimal": "70000",
                                "unscaledDecimalValue": "700000000",
                                "uiDisplayOverrideValue": "-1",
                                "scalar": "0"
                            },
                            "statRolls": 2,
                            "statRollerBoundsMin": "300000",
                            "statRollerBoundsMax": "600000"
                        },
                        {
                            "roll": [
                                "0.13040"
                            ],
                            "unscaledRollValue": [
                                "27944720"
                            ],
                            "stat": {
                                "unitStatId": 1,
                                "statValueDecimal": "2790000",
                                "unscaledDecimalValue": "27900000000",
                                "uiDisplayOverrideValue": "-1",
                                "scalar": "0"
                            },
                            "statRolls": 1,
                            "statRollerBoundsMin": "21430000",
                            "statRollerBoundsMax": "42860000"
                        },
                        {
                            "roll": [
                                "0.17071"
                            ],
                            "unscaledRollValue": [
                                "836479"
                            ],
                            "stat": {
                                "unitStatId": 42,
                                "statValueDecimal": "80000",
                                "unscaledDecimalValue": "800000000",
                                "uiDisplayOverrideValue": "-1",
                                "scalar": "0"
                            },
                            "statRolls": 1,
                            "statRollerBoundsMin": "490000",
                            "statRollerBoundsMax": "980000"
                        }
                    ],
                },
        :param comlink_data: 
        """
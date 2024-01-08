class Metadata:
    def __init__(self, comlink_payload: dict):
        self.latest_version = comlink_payload["latestGamedataVersion"]
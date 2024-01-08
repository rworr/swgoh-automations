import requests
import os

from humps import camelize
from json import dumps

from comlink import Metadata, Data, Player


def _comlink_dumps(obj: dict) -> str:
    return camelize(dumps(obj))


class Comlink:
    """
    TODO docstring
    TODO generics?
    """

    def __init__(self, uri=os.getenv("COMLINK_URI")):
        self.uri = uri

    def get_player(self, ally_code: int) -> Player:
        player_payload = {
            "payload": {
                "allyCode": str(ally_code)
            }
        }

        response = self._comlink_post(path="player", data=player_payload)
        return Player.Player(comlink_payload=response)

    def get_metadata(self) -> Metadata:
        metadata_payload = {"payload": {}}
        response = self._comlink_post(path="metadata", data=metadata_payload)
        return Metadata.Metadata(response)

    def get_data(self, metadata: Metadata) -> Data:
        data_payload = {
            "payload": {
                "version": metadata.latest_version,
                "includePveUnits": False,
            }
        }

        response = self._comlink_post(path="data", data=data_payload)
        return Data.Data(response)

    def _comlink_post(self, path: str, data: dict) -> dict:
        response = requests.post(
            url=os.path.join(self.uri, path),
            headers={"Content-Type": "application/json"},
            data=_comlink_dumps(data),
        )
        return response.json()

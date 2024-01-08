import requests
import os

from humps import camelize
from json import dumps


def _comlink_dumps(obj: dict) -> str:
    return camelize(dumps(obj))


class Comlink:
    """
    TODO docstring
    """

    def __init__(self, uri=os.getenv("COMLINK_URI")):
        self.uri = uri

    def get_player(self, ally_code: int) -> dict:
        player_payload = {
            "payload": {
                "allyCode": str(ally_code)
            }
        }

        return self._comlink_post(
            path="player",
            data=player_payload,
        )

    def _comlink_post(self, path: str, data: dict) -> dict:
        response = requests.post(
            url=os.path.join(self.uri, path),
            headers={"Content-Type": "application/json"},
            data=_comlink_dumps(data),
        )
        return response.json()

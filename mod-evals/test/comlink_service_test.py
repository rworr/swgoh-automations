import pytest

from comlink import Comlink


@pytest.fixture
def comlink():
    return Comlink("http://localhost:3200")


def test_player(comlink):
    player = comlink.get_player(245866554)
    assert player['name'] == "Hulosja"

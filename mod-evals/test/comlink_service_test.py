import pytest

from comlink import Comlink


@pytest.fixture
def comlink():
    return Comlink("http://localhost:3200")


def test_player(comlink):
    player = comlink.get_player(245866554)
    assert player.name == "Hulosja"


def test_metadata(comlink):
    metadata = comlink.get_metadata()
    assert ('.' and ':') in metadata.latest_version

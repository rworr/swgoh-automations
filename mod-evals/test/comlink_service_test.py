import pytest
from dotenv import load_dotenv

from comlink import Comlink


@pytest.fixture
def comlink():
    # TODO: skip starting comlink if already running -> use docker SDK
    load_dotenv("../.env")
    # run(["../comlink-start.sh"])
    yield Comlink()
    # run(["../comlink-stop.sh"])


def test_player(comlink):
    player = comlink.get_player(245866554)
    assert player.name == "Hulosja"


def test_metadata(comlink):
    metadata = comlink.get_metadata()
    assert ('.' and ':') in metadata.data_version


def test_localization(comlink):
    localization = comlink.get_localization()
    assert localization.get('UNIT_GREEDO_NAME') == 'Greedo'


def test_data(comlink):
    data = comlink.get_data()
    assert data.characters['ZORIIBLISS_V2:SEVEN_STAR'] == 'Zorii Bliss'


def test_guild(comlink):
    guild = comlink.get_guild("jrl9Q-_CRDGdMyNjTQH1rQ")
    assert guild.name == "MAW Chromium"
    assert len(guild.player_ids) > 0

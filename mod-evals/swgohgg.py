import re
from typing import List

import requests

GUILD_PAGE = "https://swgoh.gg/g/?page=%d"
GUILD_LINK_REGEX = r"/g/[\w-]{22}/"


def get_top_guild_ids(topn: int) -> List[str]:
    guild_ids = []
    page = 1

    while len(guild_ids) < topn:
        page_text = requests.get(GUILD_PAGE % page).text
        matches = re.findall(GUILD_LINK_REGEX, page_text)
        guilds = [match[3:-1] for match in matches]
        guild_ids.extend([guild_id for guild_id in guilds if guild_id not in guild_ids])
        page += 1

    return guild_ids[:topn]


def test_get_top_guild_ids():
    guild_ids = get_top_guild_ids(70)
    assert len(set(guild_ids)) == 70

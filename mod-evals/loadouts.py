from collections import Counter
from typing import Dict, Tuple, List

from attrs import define

import comlink
import swgohgg


@define
class AggregateCharacterLoadout:
    name: str
    top_sets: Dict[Tuple[comlink.ModSet], int]
    top_primaries: Dict[comlink.ModSlot, Dict[str, int]]
    top_secondaries: Counter[str, int]


@define
class TopCharacterLoadout:
    name: str
    sets: Tuple[comlink.ModSet]
    primaries: Dict[comlink.ModSlot, str]
    secondaries: List[str]


def identify_top_character_loadouts(top_guilds: int) -> Dict[str, TopCharacterLoadout]:
    print(f"Fetching aggregated character loadouts from top {top_guilds} guilds")
    guild_ids = swgohgg.get_top_guild_ids(top_guilds)
    aggregated_loadouts = _get_aggregated_loadouts(guild_ids)
    return {name: _get_top_loadout(aggregated_loadouts[name]) for name in aggregated_loadouts}


def _get_aggregated_loadouts(guild_ids: List[str]) -> Dict[str, AggregateCharacterLoadout]:
    aggregated_loadouts = {}
    for guild_id in guild_ids:
        guild = comlink.get_comlink().get_guild(guild_id)
        for player_id in guild.player_ids:
            player = comlink.get_comlink().get_player_by_id(player_id)
            for unit in player.roster:
                if unit.name not in aggregated_loadouts:
                    aggregated_loadouts[unit.name] = AggregateCharacterLoadout(
                        name=unit.name,
                        top_sets={},
                        top_primaries={},
                        top_secondaries=Counter({})
                    )
                _update_character_loadout(aggregated_loadouts[unit.name], unit)

    return aggregated_loadouts


def _get_top_loadout(aggregate_loadout: AggregateCharacterLoadout) -> TopCharacterLoadout:
    return TopCharacterLoadout(
        name=aggregate_loadout.name,
        sets=_get_top_entry(aggregate_loadout.top_sets),
        primaries={slot: _get_top_entry(counts) for slot, counts in aggregate_loadout.top_primaries.items()},
        secondaries=_get_top_n_entries(5, aggregate_loadout.top_secondaries)
    )


def _get_top_entry(counts: dict[any, int]):
    top_entry = None
    top_count = 0
    for entry, count in counts.items():
        if count > top_count:
            top_entry = entry
            top_count = count
    return top_entry


def _get_top_n_entries(n: int, counts: dict[any, int]) -> List:
    sorted_entries = sorted(counts.items(), key=lambda entry: entry[1], reverse=True)
    return [entry[0] for entry in sorted_entries[:n]]


def _update_character_loadout(loadout: AggregateCharacterLoadout, unit: comlink.RosterUnit):
    sets = _identify_set_combination(unit)
    primaries = _identify_primaries(unit)
    top_secondaries = _identify_top_secondaries(unit)

    loadout.top_sets[sets] = loadout.top_sets.setdefault(sets, 0) + 1
    for modslot, stat in primaries.items():
        slot_primaries = loadout.top_primaries.setdefault(modslot, {})
        slot_primaries[stat] = slot_primaries.setdefault(stat, 0) + 1
    loadout.top_secondaries += top_secondaries


def _identify_set_combination(unit: comlink.RosterUnit) -> Tuple[comlink.ModSet]:
    mod_set_counts = {}
    for mod in unit.mods:
        mod_set_counts[mod.set] = mod_set_counts.setdefault(mod.set, 0) + 1

    sets = []
    for modset, count in mod_set_counts.items():
        # TODO: fix hack for mods that need group of 2
        if modset.value in [1, 3, 5, 7, 8]:
            set_count = count // 2
            sets.extend([modset] * set_count)
        elif count == 4:
            sets.append(modset)

    return tuple(sorted(sets, key=lambda modset: modset.value))


def _identify_primaries(unit: comlink.RosterUnit) -> Dict[comlink.ModSlot, str]:
    return {mod.slot: mod.primary for mod in unit.mods}


def _identify_top_secondaries(unit: comlink.RosterUnit) -> Counter:
    secondaries = Counter({})
    for mod in unit.mods:
        for secondary in mod.secondaries:
            secondaries[secondary.name] = secondaries.setdefault(secondary.name, 0) + 1
    return secondaries

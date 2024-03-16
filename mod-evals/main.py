import csv
import os.path
from typing import Dict

from dotenv import load_dotenv

import comlink
import loadouts


def export_to_csv(top_loadouts: Dict[str, loadouts.TopCharacterLoadout]):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "mod_loadouts.csv")
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ["Character"] +
            [f"Set {n}" for n in range(1, 4)] +
            [slot.name.capitalize() for slot in comlink.ModSlot] +
            [f"Secondary {n}" for n in range(1, 6)]
        )

        for character, loadout in top_loadouts.items():
            # TODO: fix newer characters without data
            if len(loadout.sets) < 2:
                continue

            sorted_primaries = sorted(loadout.primaries.items(), key=lambda entry: entry[0].value)
            csv_writer.writerow(
                [character] +
                [modset.name.capitalize().replace("_", ' ') for modset in loadout.sets] +
                ([] if len(loadout.sets) == 3 else [""]) +
                [stat.capitalize() for slot, stat in sorted_primaries] +
                loadout.secondaries
            )


if __name__ == '__main__':
    load_dotenv()
    top_loadouts = loadouts.identify_top_character_loadouts(50)
    export_to_csv(top_loadouts)
    comlink.stop_comlink()

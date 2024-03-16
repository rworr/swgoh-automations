from dotenv import load_dotenv

import comlink
import loadouts

if __name__ == '__main__':
    load_dotenv()
    top_loadouts = loadouts.identify_top_character_loadouts(1)
    comlink.stop_comlink()

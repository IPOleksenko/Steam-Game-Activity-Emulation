import logging
import time

from utils.dll import DLL
from utils.steamworks import Steamworks

from config import CALLBACK_SLEEP_INTERVAL

def run(steam_game_id: list = ["480"]):
    try:
        DLL.initialize()
        steamworks = Steamworks(SteamAppId=steam_game_id[0], SteamGameId=steam_game_id[0])
        
        while True:
            steamworks.SteamAPI_RunCallbacks()
            time.sleep(CALLBACK_SLEEP_INTERVAL)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return
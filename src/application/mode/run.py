import logging
import time

from utils.dll import DLL
from utils.steamworks import Steamworks

def run(steam_game_id: list = ["480"]):
    try:
        DLL.initialize()
        steamworks = Steamworks(SteamAppId=steam_game_id[0], SteamGameId=steam_game_id[0])
        
        while True:
            steamworks.SteamAPI_RunCallbacks()
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return
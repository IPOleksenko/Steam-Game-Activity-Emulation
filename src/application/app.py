import time
import logging

from utils import Steamworks

def app():
    try:
        steamworks = Steamworks()
        
        for _ in range(100):
            steamworks.SteamAPI_RunCallbacks()
            time.sleep(0.1)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return

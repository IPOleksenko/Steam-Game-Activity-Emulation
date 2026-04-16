import logging
import time

from utils import DLL, Steamworks
import config

def run(steam_game_id: list = ["480"], callback_sleep_interval=None, stop_event=None):
    try:
        DLL.initialize()

        steamworks = Steamworks(
            SteamAppId=steam_game_id[0],
            SteamGameId=steam_game_id[0]
        )

        if stop_event is None:
            raise ValueError("stop_event must be provided")

        if callback_sleep_interval:
            logging.info(f"Starting SteamAPI_RunCallbacks loop with interval: {callback_sleep_interval} seconds")
            while not stop_event.is_set():
                steamworks.SteamAPI_RunCallbacks()
                time.sleep(callback_sleep_interval)
        else:
            logging.info("SteamAPI_RunCallbacks loop is disabled (callback_sleep_interval is None)")
            stop_event.wait()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
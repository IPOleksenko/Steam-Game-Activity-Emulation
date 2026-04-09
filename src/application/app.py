import logging
from multiprocessing import Process
from threading import Event
import pystray
from PIL import Image

from .mode import run
from config import ICON_PATH

processes = []
stop_event = Event()


def worker(game_id: str):
    try:
        run(steam_game_id=[game_id])
    except Exception as e:
        logging.error(f"Worker error for {game_id}: {e}")


def stop_all(icon=None, item=None):
    logging.info("Stopping all processes...")

    stop_event.set()

    for p in processes:
        if p.is_alive():
            p.terminate()

    for p in processes:
        p.join(timeout=2)

    processes.clear()

    if icon is not None:
        icon.stop()


def app(mode: str = "run", steam_game_id: list = None):
    if steam_game_id is None:
        steam_game_id = ["480"]

    try:
        logging.info(f"Starting app with mode: {mode} and Steam Game ID(s): {steam_game_id}")

        if mode == "run":
            for game_id in steam_game_id:
                p = Process(target=worker, args=(game_id,))
                p.start()
                processes.append(p)
                logging.info(f"Process started for Game ID {game_id}")

            menu = pystray.Menu(
                pystray.MenuItem("Exit", stop_all)
            )

            icon = pystray.Icon(
                "steam_game_activity_emulation",
                Image.open(ICON_PATH),
                "Steam Game Activity Emulation",
                menu
            )

            icon.run()

    except Exception as e:
        logging.error(f"An error occurred in app: {e}")
        stop_all()
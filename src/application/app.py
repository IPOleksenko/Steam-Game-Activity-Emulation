import logging
from multiprocessing import Process
from threading import Event, Timer
import pystray
from PIL import Image

from utils import run
from config import APP_NAME, APP_SLOG, ICON_PATH

TIME_RESTART_DELAY = 30  # seconds
processes = []
stop_event = Event()
current_steam_game_ids = []


def worker(game_id: str):
    try:
        run(steam_game_id=[game_id])
    except Exception as e:
        logging.error(f"Worker error for {game_id}: {e}")


def start_processes(steam_game_id: list):
    global processes, current_steam_game_ids

    current_steam_game_ids = steam_game_id
    processes = []

    for game_id in steam_game_id:
        p = Process(target=worker, args=(game_id,))
        p.start()
        processes.append(p)
        logging.info(f"Process started for Game ID {game_id}")


def stop_all_processes():
    global processes

    logging.info("Stopping all processes...")

    stop_event.set()

    for p in processes:
        if p.is_alive():
            p.terminate()

    for p in processes:
        p.join(timeout=2)

    processes.clear()
    stop_event.clear()


def restart_all(icon=None, item=None):
    logging.info("Restart requested...")

    stop_all_processes()

    def delayed_start():
        logging.info(f"Restarting processes after {TIME_RESTART_DELAY} seconds...")
        start_processes(current_steam_game_ids)

    Timer(TIME_RESTART_DELAY, delayed_start).start()


def stop_and_exit(icon=None, item=None):
    stop_all_processes()
    if icon is not None:
        icon.stop()


def app(mode: str = "run", steam_game_id: list = None):
    if steam_game_id is None:
        steam_game_id = ["480"]

    logging.info(f"Starting app with mode: {mode} and Steam Game ID(s): {steam_game_id}")

    if mode == "console":
        start_processes(steam_game_id)

        try:
            while True:
                for p in processes:
                    p.join(timeout=1)
        except KeyboardInterrupt:
            logging.info("Ctrl+C received, shutting down...")
            stop_all_processes()

    elif mode == "run":
        try:
            start_processes(steam_game_id)

            menu = pystray.Menu(
                pystray.MenuItem("Restart", restart_all),
                pystray.MenuItem("Exit", stop_and_exit),
            )

            icon = pystray.Icon(
                APP_SLOG,
                Image.open(ICON_PATH),
                APP_NAME,
                menu
            )

            icon.run()

        except Exception as e:
            logging.error(f"An error occurred in app: {e}")
            stop_all_processes()
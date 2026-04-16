import argparse
import logging
from multiprocessing import Process, Event
from threading import Timer
import pystray
from PIL import Image
import sys
import subprocess
import os

from utils import run, setup_logging, start_restart_schedulers
from config import APP_NAME, APP_SLOG, ICON_PATH, MOD_TYPES
import config

processes = []
stop_event = Event()
current_steam_game_ids = []


def detach_console(args):
    if args.detached:
        return

    cmd = [sys.executable, *sys.argv, "--detached"]

    if os.name == "nt":
        subprocess.Popen(
            ["pythonw", *sys.argv, "--detached"],
            close_fds=True
        )
    else:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True
        )

    sys.exit()

def worker(game_id: str, callback_sleep_interval: float = None):
    try:
        setup_logging()
        run(steam_game_id=[game_id], callback_sleep_interval=callback_sleep_interval, stop_event=stop_event)
    except Exception as e:
        logging.error(f"Worker error for {game_id}: {e}")


def start_processes(steam_game_id: list):
    global processes, current_steam_game_ids

    current_steam_game_ids = steam_game_id
    processes = []

    for game_id in steam_game_id:
        p = Process(target=worker, args=(game_id, config.callback_sleep_interval))
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
        logging.info(f"Restarting processes after {config.time_restart_delay} seconds...")
        start_processes(current_steam_game_ids)

    Timer(config.time_restart_delay, delayed_start).start()


def stop_and_exit(icon=None, item=None):
    stop_all_processes()
    if icon is not None:
        icon.stop()


def app(mode: str = MOD_TYPES[0], steam_game_id: list = None, args: argparse.Namespace = None):
    if steam_game_id is None:
        steam_game_id = ["480"]

    logging.info(f"Starting app with mode: {mode} and Steam Game ID(s): {steam_game_id}")

    try:
        detach_console(args)
        start_processes(steam_game_id)
        start_restart_schedulers(restart_all, restart_interval=config.restart_interval, restart_time=config.restart_time)
    except Exception as e:
        logging.error(f"An error occurred during app initialization: {e}")

    if mode == MOD_TYPES[0]: # tray
        try:
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

    elif mode == MOD_TYPES[1]: # console
        try:
            while True:
                for p in processes:
                    p.join(timeout=1)
        except KeyboardInterrupt:
            logging.info("Ctrl+C received, shutting down...")
            stop_all_processes()
        except Exception as e:
            logging.error(f"An error occurred in app: {e}")
            stop_all_processes()
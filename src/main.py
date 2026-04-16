import logging
import argparse

from application import app
from config import MOD_TYPES
import config
from utils import setup_logging, argparse_hhmm_time 

def parse_arguments():
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "--mode",
        type=str.lower,
        choices=MOD_TYPES,
        default=MOD_TYPES[0],
        help="Mode to run the application in (default: %(default)s)"
    )
    pre_args, _ = pre_parser.parse_known_args()

    parser = argparse.ArgumentParser(description="Run the application", parents=[pre_parser])
    parser.add_argument(
        "--steam-game-id",
        type=str,
        nargs="+",
        default=["480"],
        help="One or more Steam Game IDs to emulate (default: %(default)s)"
    )

    parser.add_argument(
        "--detached",
        action="store_true",
        default= False if pre_args.mode == MOD_TYPES[0] else True,
        help=f"Run the application in detached mode (default: %(default)s for '{MOD_TYPES[0]}' mode, True for all other modes)"
    )

    parser.add_argument(
        "--time_restart_delay",
        type=float,
        default=config.time_restart_delay,
        help="Delay in seconds before restarting processes after a restart request (default: %(default)s)"
    )

    parser.add_argument(
        "--callback_sleep_interval",
        type=float,
        default=config.callback_sleep_interval,
        help="Sleep interval in seconds for SteamAPI_RunCallbacks loop (default: %(default)s. If None, the callback is not used)"
    )

    parser.add_argument(
        "--restart_interval",
        type=float,
        default=config.restart_interval,
        help="Interval in seconds for automatic restarts (default: %(default)s. If None, automatic restarts are disabled)"
    )

    parser.add_argument(
        "--restart_time",
        type=argparse_hhmm_time,
        nargs="+",
        default=config.restart_time,
        help="One or more scheduled restart times in HH:MM format (default: %(default)s. If None, scheduled restarts are disabled)"
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    logging.info("Starting the application with arguments: %s", args)

    mode = args.mode
    logging.info("Running in %s mode", mode)

    steam_game_id = args.steam_game_id
    logging.info("Emulating Steam Game ID(s): %s", steam_game_id)

    config.time_restart_delay = args.time_restart_delay
    logging.info(f"Using time_restart_delay: {config.time_restart_delay} {'seconds' if config.time_restart_delay else ''}")

    config.callback_sleep_interval = args.callback_sleep_interval
    logging.info(f"Using callback_sleep_interval: {config.callback_sleep_interval} {'seconds' if config.callback_sleep_interval else ''}")

    config.restart_interval = args.restart_interval
    logging.info(f"Using restart_interval: {config.restart_interval} {'seconds' if config.restart_interval else ''}")
    
    config.restart_time = args.restart_time
    logging.info(f"Using restart_time: {config.restart_time}")

    app(mode=mode, steam_game_id=steam_game_id, args=args)

if __name__ == "__main__":
    setup_logging()
    main()
import logging
import argparse

from application import app
from config import MOD_TYPES
import config

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
        help="Sleep interval in seconds for SteamAPI_RunCallbacks loop (default: %(default)s)"
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
    logging.info(f"Using time_restart_delay: {config.time_restart_delay} seconds")

    config.callback_sleep_interval = args.callback_sleep_interval
    logging.info(f"Using callback_sleep_interval: {config.callback_sleep_interval} seconds")

    app(mode=mode, steam_game_id=steam_game_id, args=args)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
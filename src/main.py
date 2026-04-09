import logging
import sys

from application import app

MOD_TYPE = ["run"]

def main(*args, **kwargs):
    mode = args[0] if args and args[0] in MOD_TYPE else "run"
    if not args or args[0] not in MOD_TYPE:
        logging.warning(f"Invalid or missing mode. Defaulting to 'run'.")

    raw_ids = args[1:] if len(args) > 1 else []
    steam_game_id = [x for x in raw_ids if x.isdigit()]

    if not raw_ids:
        logging.info("No Steam Game ID provided. Using default: 480 (Spacewar).")
    if len(steam_game_id) != len(raw_ids):
        invalid = set(raw_ids) - set(steam_game_id)
        for x in invalid:
            logging.warning(f"Invalid Steam Game ID '{x}' removed from the list.")

    if not steam_game_id:
        steam_game_id = ["480"]
        logging.warning("No valid Steam Game IDs provided. Using default: 480 (Spacewar).")

    app(mode=mode, steam_game_id=steam_game_id)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(*sys.argv)

from pathlib import Path
import os

APP_NAME = "Steam Game Activity Emulation"
APP_SLOG = "steam_game_activity_emulation"

MOD_TYPES = ["tray", "console"]

ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_PATH = Path(os.path.join(ROOT_PATH, 'assets'))
ICON_PATH = Path(os.path.join(ASSETS_PATH, 'icon.png'))
SRC_PATH = Path(os.path.join(ROOT_PATH, 'src'))
STEAMWORKS_SDK_PATH = Path(os.path.join(ROOT_PATH, 'steamworks_sdk_155'))

time_restart_delay = 30.0
callback_sleep_interval = None
restart_interval = None
restart_time = None
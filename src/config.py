from pathlib import Path
import os


ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_PATH = Path(os.path.join(ROOT_PATH, 'src'))
STEAMWORKS_SDK_PATH = Path(os.path.join(ROOT_PATH, 'steamworks_sdk_155'))
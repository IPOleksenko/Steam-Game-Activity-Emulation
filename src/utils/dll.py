import ctypes
import logging
import sys
import os
import platform

from config import STEAMWORKS_SDK_PATH

class DLL:
    _steamworks_dll_path = None
    _steamworks_dll = None

    @staticmethod
    def _set_steamworks_dll_path():
        current_platform = platform.system()
        arch, _ = platform.architecture()

        if current_platform == "Windows":
            if arch == "64bit":
                DLL._steamworks_dll_path = STEAMWORKS_SDK_PATH / "win64" / "steam_api64.dll"
            else:
                DLL._steamworks_dll_path = STEAMWORKS_SDK_PATH / "steam_api.dll"
        elif current_platform == "Linux":
            if arch == "64bit":
                DLL._steamworks_dll_path = STEAMWORKS_SDK_PATH / "linux64" / "libsteam_api.so"
            else:
                DLL._steamworks_dll_path = STEAMWORKS_SDK_PATH / "linux" / "libsteam_api.so"
        elif current_platform == "Darwin":
            DLL._steamworks_dll_path = STEAMWORKS_SDK_PATH / "osx" / "libsteam_api.dylib"

    @staticmethod
    def get_steamworks_dll_path():
        return DLL._steamworks_dll_path
    
    @staticmethod
    def initialize():
        try:
            DLL._set_steamworks_dll_path()
            DLL._steamworks_dll = ctypes.CDLL(str(DLL.get_steamworks_dll_path()))
            logging.info(f"Successfully loaded Steamworks DLL from {DLL.get_steamworks_dll_path()}")
            return True
        except Exception as e:
            logging.error(f"Failed to load Steamworks DLL: {e}")
            return False

    @staticmethod
    def get_steamworks_dll():
        if DLL._steamworks_dll is None:
            raise Exception("DLL not initialized. Call DLL.initialize() first.")
        return DLL._steamworks_dll
import logging
import os

from utils import DLL

class Steamworks:
    def __init__(self, SteamAppId: str = "480", SteamGameId: str = "480"):
        os.environ["SteamAppId"] = SteamAppId
        os.environ["SteamGameId"] = SteamGameId
        
        self.sdk = DLL.get_steamworks_dll()
        self.SteamAPI_Init()
    
    def __del__(self):
        self.SteamAPI_Shutdown()
    
    def SteamAPI_Init(self):
        logging.info(f"SteamAPI_Init() : {self.sdk.SteamAPI_Init()}")

    def SteamAPI_Shutdown(self):
        logging.info(f"SteamAPI_Shutdown() : {self.sdk.SteamAPI_Shutdown()}")

    def SteamAPI_RunCallbacks(self, with_logging: bool = False):
        result = self.sdk.SteamAPI_RunCallbacks()
        if with_logging:
            logging.info(f"SteamAPI_RunCallbacks() : {result}")
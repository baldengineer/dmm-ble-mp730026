from fastapi import logger as _logger
from obswebsocket import obsws
from obswebsocket import requests
from obswebsocket.exceptions import ConnectionFailure

from settings import OBS_Settings

logger = _logger.logger
logger.setLevel(20)


class OBS:
    def __init__(self):
        self.enabled = OBS_Settings.enabled
        self.__connected = False
        if self.enabled:
            self.client = obsws(OBS_Settings.ip, OBS_Settings.ws_port, OBS_Settings.secret)

    @property
    def connected(self) -> bool:
        if not self.__connected:
            try:
                self.client.connect()
                self.__connected = True
                logger.info("OBS Connected")
            except ConnectionFailure:
                self.__connected = False
                logger.warning("OBS failed to connect.")

        return self.__connected

    def send(self, enabled: bool, scene: str, source: str) -> None:
        """
        Sends a command to OBS to show or hide the source if connected
        Returns None
        """

        if self.connected:
            self.client.call(requests.SetSceneItemRender(source, enabled, scene))
            logger.info

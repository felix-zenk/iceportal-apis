from datetime import datetime
from json import JSONDecodeError
from threading import Thread
from time import sleep
from typing import Tuple

from requests import RequestException, get

from .exceptions import (NetworkException, ApiException, NotOnTrainException)
from .types import InterfaceStatus


class ApiInterface:
    def __init__(self):
        self.interface_status: InterfaceStatus = InterfaceStatus.IDLE
        self.status: dict = {}
        self.trip: dict = {}
        self.connections: dict = {}
        self.stations: dict = {}
        self.eva_nr_2_name: dict = {}
        self.name_2_eva_nr: dict = {}
        self._auto_refresh_thread: Thread = Thread(target=self._auto_refresh, name="ApiInterfaceConnectionThread")
        self._auto_refresh_switch: bool = False
        self._AUTO_REFRESH_INTERVAL: int = 1
        self.refresh()

    def _request_json(self, url: str) -> dict:
        """Requests data from 'url' and parses it as a dictionary
        """
        self.interface_status = InterfaceStatus.FETCHING
        try:
            data = get(url)
        except RequestException:
            self.interface_status = InterfaceStatus.ERROR
            raise NetworkException(url)
        try:
            j_data = data.json()
            self.interface_status = InterfaceStatus.IDLE
            return j_data
        except JSONDecodeError:
            self.interface_status = InterfaceStatus.ERROR
            raise NotOnTrainException()

    def _get_status(self) -> dict:
        """Returns the status data.
        """
        return self._request_json(URL_STATUS)

    def _get_trip(self) -> dict:
        """Returns the trip data.
        """
        return self._request_json(URL_TRIP)

    def _get_connections(self, eva_nr: str) -> dict:
        """
        Gets connecting trains for eva_nr
        :param eva_nr: The stations evaNr
        :type eva_nr: str
        :return: The connecting trains
        :rtype: dict
        """
        return self._request_json(URL_CONNECTIONS.format(eva_nr))

    def _get_pois(self, start_pos: Tuple[str, str], end_pos: Tuple[str, str]) -> dict:
        """
        Returns points of interest in the rectangular area spanned by start_pos and end_pos
        :param start_pos: The first corner position
        :type start_pos: Tuple
        :param end_pos: The second corner position
        :type end_pos: Tuple
        :return: dict
        """
        return self._request_json(URL_POIS.format(start_pos[0], start_pos[1], end_pos[0], end_pos[1]))

    def refresh(self) -> None:
        """
        Refreshes all data
        """
        self.status = self._get_status()
        self.trip = self._get_trip()
        for eva_nr, name in [(stop["station"]["evaNr"], stop["station"]["name"])
                             for stop in self.trip["trip"]["stops"]]:
            self.name_2_eva_nr[name] = eva_nr
            self.eva_nr_2_name[eva_nr] = name
            self.connections[eva_nr] = self._get_connections(eva_nr)

    def _auto_refresh(self) -> None:
        while self._auto_refresh_switch:
            start = datetime.now()
            try:
                self.refresh()
            except ApiException as ex:
                self._auto_refresh_switch = False
                raise ex
            delta = datetime.now() - start
            sleep(0 if delta.total_seconds() > self._AUTO_REFRESH_INTERVAL
                  else self._AUTO_REFRESH_INTERVAL - delta.seconds - delta.microseconds / 1000000)

    def set_auto_refresh(self, auto_refresh: bool, interval: int = None):
        if interval:
            self._AUTO_REFRESH_INTERVAL = interval
        if auto_refresh:
            self._auto_refresh_switch: bool = True
            self._auto_refresh_thread = Thread(target=self._auto_refresh, name="ApiInterfaceConnectionThread")
            self._auto_refresh_thread.start()
        else:
            self._auto_refresh_switch = False
            if self._auto_refresh_thread.is_alive():
                self._auto_refresh_thread.join()

import asyncio
import datetime
import json
import os
import threading
import time
import typing
import aiohttp
import requests

from .constants import (URL_STATUS, URL_TRIP, URL_CONNECTIONS, URL_POIS, URL_BAP, URL_AUDIOBOOKS, BASE_URL)
from .exceptions import (NetworkException, ApiException, NotOnTrainException)
from .mocking import StaticSimulation, DynamicSimulation
from .types import InterfaceStatus


headers = {"User-Agent": "python:iceportal_apis"}  # Header to inform the api that this request was sent via this module


class Requestable:
    def __init__(self):
        pass

    def get(self, url, **kwargs):
        return requests.get(url, headers=headers, **kwargs)

    def get_json(self, url, **kwargs):
        try:
            response = self.get(url, **kwargs)
            try:
                return response.json()
            except json.JSONDecodeError:
                raise NotOnTrainException()
        except requests.exceptions.RequestException:
            raise NetworkException()


class ApiInterface:
    def __init__(self):
        self.interface_status: InterfaceStatus = InterfaceStatus.IDLE
        self.status: dict = {}
        self.trip: dict = {}
        self.connections: dict = {}
        self.stations: dict = {}
        self.bap: dict = {}
        self.pois: typing.List = []
        self.eva_nr_2_name: dict = {}
        self.name_2_eva_nr: dict = {}
        self._event_loop = asyncio.get_event_loop()
        self._auto_refresh_thread: threading.Thread = threading.Thread(target=None, daemon=True)
        self._auto_refresh_switch: bool = False
        self._AUTO_REFRESH_INTERVAL: int = 1
        self._refresh_lock = threading.Lock()
        self.refresh()

    async def _request_json(self, url: str) -> dict:
        """
        Requests data from 'url' and parses it as a dictionary
        """
        self.interface_status = InterfaceStatus.FETCHING
        async with aiohttp.ClientSession(loop=self._event_loop) as session:
            async with session.get(url, headers=headers) as response:
                try:
                    return await response.json()
                except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
                    raise NotOnTrainException() from e
                except aiohttp.ClientError as e:
                    raise NetworkException from e

    async def _get_status(self) -> None:
        """
        Refreshes the status data.
        """
        self.status = await self._request_json(URL_STATUS)

    async def _get_trip(self):
        """
        Refreshes the trip data.
        """
        self.trip = await self._request_json(URL_TRIP)

    async def _get_connections(self, eva_nr: str):
        """
        Refreshes connecting trains for eva_nr
        :param eva_nr: The stations evaNr
        :type eva_nr: str
        """
        self.connections[eva_nr] = await self._request_json(URL_CONNECTIONS.format(eva_nr))

    async def _get_bap(self) -> None:
        """
        Refreshes data for bap service
        """
        self.bap = await self._request_json(URL_BAP) \
            if self.status["bapInstalled"] \
            else {"bapServiceStatus": "INACTIVE", "status": False}

    def _get_pois(self, start_pos: typing.Tuple[float, float], end_pos: typing.Tuple[float, float]) -> dict:
        """
        Refreshes points of interest in the rectangular area spanned by start_pos and end_pos
        :param start_pos: The first corner position
        :type start_pos: Tuple
        :param end_pos: The second corner position
        :type end_pos: Tuple
        """
        return {
            'start_pos': start_pos,
            'end_pos': end_pos,
            'data': self._request_json(URL_POIS.format(start_pos[0], start_pos[1], end_pos[0], end_pos[1]))
        }

    def refresh(self) -> None:
        """
        Refreshes all data
        """
        async def refresh_async():
            if self.trip == {}:  # First request -> No data for _get_connections yet
                await asyncio.gather(self._get_status(), self._get_trip())
                await asyncio.gather(*[self._get_connections(url) for url in list(self.eva_nr_2_name.keys())],
                                     self._get_bap())
            else:
                await asyncio.gather(self._get_status(), self._get_trip(), self._get_bap(),
                                     *[self._get_connections(url) for url in list(self.eva_nr_2_name.keys())]
                                     )

        # Make thread safe
        self._refresh_lock.acquire()
        # Run async
        try:
            self._event_loop.run_until_complete(refresh_async())
            # Refresh lookup dicts
            try:
                for eva_nr, name in [(stop["station"]["evaNr"], stop["station"]["name"])
                                     for stop in self.trip["trip"]["stops"]]:
                    self.name_2_eva_nr[name] = eva_nr
                    self.eva_nr_2_name[eva_nr] = name
            except KeyError as e:
                print("Key error: ", e)
        except (NotOnTrainException, NetworkException):
            raise
        finally:
            self._refresh_lock.release()

    def _auto_refresh(self) -> None:
        while self._auto_refresh_switch:
            start = datetime.datetime.now()
            try:
                self.refresh()
            except ApiException:
                self._auto_refresh_switch = False
                raise
            delta = datetime.datetime.now() - start
            time.sleep(0 if delta.total_seconds() > self._AUTO_REFRESH_INTERVAL
                       else self._AUTO_REFRESH_INTERVAL - delta.seconds - delta.microseconds / 1000000)

    def set_auto_refresh(self, auto_refresh: bool, interval: int = None):
        if interval:
            self._AUTO_REFRESH_INTERVAL = interval
        if auto_refresh:
            self._auto_refresh_switch: bool = True
            self._auto_refresh_thread = threading.Thread(target=self._auto_refresh,
                                                         name=self.__class__.__name__+"ConnectionThread",
                                                         daemon=True)
            self._auto_refresh_thread.start()
        else:
            self._auto_refresh_switch = False


class SynchronousApiInterface(ApiInterface, Requestable):
    def __init__(self):
        super(SynchronousApiInterface, self).__init__()

    def _request_json(self, url: str) -> dict:
        return self.get_json(url)

    def _get_status(self) -> None:
        self.status = self._request_json(URL_STATUS)

    def _get_trip(self):
        self.trip = self._request_json(URL_TRIP)

    def _get_connections(self, eva_nr: str):
        self.connections[eva_nr] = self._request_json(URL_CONNECTIONS.format(eva_nr))

    def refresh(self) -> None:
        self._get_status()
        self._get_trip()
        for eva_nr, name in [(stop["station"]["evaNr"], stop["station"]["name"])
                             for stop in self.trip["trip"]["stops"]]:
            self.name_2_eva_nr[name] = eva_nr
            self.eva_nr_2_name[eva_nr] = name
            self._get_connections(eva_nr)


class TestInterface(ApiInterface):
    def __init__(self,
                 simulation_type: typing.Type[typing.Union[StaticSimulation, DynamicSimulation]] = StaticSimulation):
        self.simulation = simulation_type()
        self.simulation.start()
        super(TestInterface, self).__init__()

    def __del__(self):
        try:
            self.simulation.stop()
        except AttributeError:
            pass

    def _get_status(self) -> dict:
        return self.simulation.get_status()

    def _get_trip(self) -> dict:
        return self.simulation.get_trip()

    def _get_connections(self, eva_nr: str) -> dict:
        return self.simulation.get_connections(eva_nr)

    def refresh(self) -> None:
        self.status = self._get_status()
        self.trip = self._get_trip()
        for stop in self.trip["trip"]["stops"]:
            eva_nr = stop["station"]["evaNr"]
            name = stop["station"]["name"]
            self.name_2_eva_nr[name] = eva_nr
            self.eva_nr_2_name[eva_nr] = name
            self.stations[eva_nr] = stop
            self.connections[eva_nr] = self._get_connections(eva_nr)

    def set_auto_refresh(self, auto_refresh: bool, interval: int = None):
        super(TestInterface, self).set_auto_refresh(auto_refresh=auto_refresh, interval=interval)


class Part(Requestable):
    def __init__(self, filename, url, collect: bool = False):
        super().__init__()
        self.filename = filename
        self.url = url
        self.content = self.get(BASE_URL+self.url).content if collect else None


class Media(Requestable):
    def __init__(self, title, url):
        super().__init__()
        self.title = title
        self.url = url
        self.parts = self._get_parts()

    def _get_parts(self):
        return list(
            [Part(file["title"]+"."+file["path"].split(".")[-1], file["path"])
             for file in self.get_json(self.url)["files"]
             ])


class PageIndex(Requestable):
    def __init__(self, url):
        super().__init__()
        self.data = self.get_json(url)

    def list(self) -> typing.List[Media]:
        return list(
            [Media(media["title"], media["navigation"]["href"]) for media in self.data["teaserGroups"][0]["items"]]
        )


class MediaInterface:
    def __init__(self):
        self.audiobooks = PageIndex(URL_AUDIOBOOKS)

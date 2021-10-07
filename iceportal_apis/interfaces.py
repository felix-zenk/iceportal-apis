import asyncio
from datetime import datetime
from json import JSONDecodeError
from threading import Thread
from time import sleep
from typing import Tuple, Union, Type, List

from aiohttp import ClientSession, ContentTypeError, ClientError

from .constants import (URL_STATUS, URL_TRIP, URL_CONNECTIONS, URL_POIS)
from .exceptions import (NetworkException, ApiException, NotOnTrainException)
from .mocking import StaticSimulation, DynamicSimulation
from .types import InterfaceStatus


class ApiInterface:
    def __init__(self):
        self.interface_status: InterfaceStatus = InterfaceStatus.IDLE
        self.status: dict = {}
        self.trip: dict = {}
        self.connections: dict = {}
        self.stations: dict = {}
        self.pois: List = []
        self.eva_nr_2_name: dict = {}
        self.name_2_eva_nr: dict = {}
        self._auto_refresh_thread: Thread = Thread(target=None, daemon=True)
        self._auto_refresh_switch: bool = False
        self._AUTO_REFRESH_INTERVAL: int = 1
        self._event_loop = asyncio.get_event_loop()
        self.refresh()

    async def _request_json(self, url: str) -> dict:
        """Requests data from 'url' and parses it as a dictionary
        """
        self.interface_status = InterfaceStatus.FETCHING
        async with ClientSession(loop=self._event_loop) as session:
            async with session.get(url) as response:
                try:
                    return await response.json()
                except (JSONDecodeError, ContentTypeError) as e:
                    raise NotOnTrainException() from e
                except ClientError as e:
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

    async def _get_pois(self, start_pos: Tuple[str, str], end_pos: Tuple[str, str]):
        """
        Refreshes points of interest in the rectangular area spanned by start_pos and end_pos
        :param start_pos: The first corner position
        :type start_pos: Tuple
        :param end_pos: The second corner position
        :type end_pos: Tuple
        """
        self.pois.append({
            'start_pos': start_pos,
            'end_pos': end_pos,
            'data': await self._request_json(URL_POIS.format(start_pos[0], start_pos[1], end_pos[0], end_pos[1]))
        })

    def refresh(self) -> None:
        """
        Refreshes all data
        """
        async def refresh_async():
            tasks = [self._get_status(), self._get_trip()]
            tasks.extend([self._get_connections(url) for url in list(self.eva_nr_2_name.keys())])
            await asyncio.gather(*tasks)

        # Run async
        # TODO Testing on a train needed
        try:
            self._event_loop.run_until_complete(refresh_async())
            # Refresh lookup dicts
            try:
                for eva_nr, name in [(stop["station"]["evaNr"], stop["station"]["name"])
                                     for stop in self.trip["trip"]["stops"]]:
                    self.name_2_eva_nr[name] = eva_nr
                    self.eva_nr_2_name[eva_nr] = name
            except KeyError:
                pass
        except (NotOnTrainException, NetworkException):
            raise

    def _auto_refresh(self) -> None:
        while self._auto_refresh_switch:
            start = datetime.now()
            try:
                self.refresh()
            except ApiException:
                self._auto_refresh_switch = False
                raise
            delta = datetime.now() - start
            sleep(0 if delta.total_seconds() > self._AUTO_REFRESH_INTERVAL
                  else self._AUTO_REFRESH_INTERVAL - delta.seconds - delta.microseconds / 1000000)

    def set_auto_refresh(self, auto_refresh: bool, interval: int = None):
        if interval:
            self._AUTO_REFRESH_INTERVAL = interval
        if auto_refresh:
            self._auto_refresh_switch: bool = True
            self._auto_refresh_thread = Thread(target=self._auto_refresh,
                                               name=self.__class__.__name__+"ConnectionThread",
                                               daemon=True)
            self._auto_refresh_thread.start()
        else:
            self._auto_refresh_switch = False
            # WONT BE NEEDED BECAUSE THREAD IS DAEMON THREAD
            # if self._auto_refresh_thread.is_alive():
            #    self._auto_refresh_thread.join()


class TestInterface(ApiInterface):
    def __init__(self, simulation_type: Type[Union[StaticSimulation, DynamicSimulation]] = StaticSimulation):
        self.simulation = simulation_type()
        self.simulation.start()
        super(TestInterface, self).__init__()

    def __del__(self):
        try:
            self.simulation.stop()
        except AttributeError:
            pass
        super(TestInterface, self).__del__()

    def _get_status(self) -> dict:
        return self.simulation.get_status()

    def _get_trip(self) -> dict:
        return self.simulation.get_trip()

    def _get_connections(self, eva_nr: str) -> dict:
        return self.simulation.get_connections(eva_nr)

    def refresh(self) -> None:
        self.status = self._get_status()
        self.trip = self._get_trip()
        for eva_nr, name in [(stop["station"]["evaNr"], stop["station"]["name"])
                             for stop in self.trip["trip"]["stops"]]:
            self.name_2_eva_nr[name] = eva_nr
            self.eva_nr_2_name[eva_nr] = name
            self.connections[eva_nr] = self._get_connections(eva_nr)

    def set_auto_refresh(self, auto_refresh: bool, interval: int = None):
        super(TestInterface, self).set_auto_refresh(auto_refresh=auto_refresh, interval=interval)

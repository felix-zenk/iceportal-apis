from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from ..interfaces import ApiInterface
from .data import (STATIC_STATUS, STATIC_TRIP, STATIC_CONNECTIONS)


class Simulation:
    def __init__(self):
        self.simulation_thread = Thread(target=self._simulate, name=self.__class__.__name__ + "Thread")
        self._running = False
        self._interval = timedelta(seconds=1)
        self._status = STATIC_STATUS
        self._trip = STATIC_TRIP
        self._connections = STATIC_CONNECTIONS

    def start(self):
        self.simulation_thread.start()

    def stop(self):
        self._running = False
        self.simulation_thread.join()

    def get_status(self):
        return self._status

    def get_trip(self):
        return self._trip

    def get_connections(self, eva_nr):
        return self._connections

    def _simulate(self):
        self._running = True


class StaticSimulation(Simulation):
    def __init__(self):
        """
        Static simulation of the api
        """
        super(StaticSimulation, self).__init__()


class DynamicSimulation(Simulation):
    def __init__(self):
        """
        Simulates the behaviour of the onboard api dynamically
        """
        super(DynamicSimulation, self).__init__()
        raise NotImplementedError()  # Use is not recommended but possible

    def _refresh_values(self):
        # raise NotImplementedError()
        pass

    def _simulate(self):
        self._running = True
        while self._running:
            start = datetime.now()
            self._refresh_values()
            while (delta := (datetime.now() - start)) < self._interval:
                if not self._running:
                    break
                remaining_time = self._interval - delta
                remaining_milliseconds = remaining_time.microseconds / 1000.0 + 1000 * remaining_time.seconds
                sleep(0.1 if remaining_milliseconds > 100 else remaining_milliseconds / 1000.0)


class TestInterface(ApiInterface):
    def __init__(self):
        self.simulation = Simulation()
        super(TestInterface, self).__init__()

    def _get_status(self) -> dict:
        return self.simulation.get_status()

    def _get_trip(self) -> dict:
        return self.simulation.get_trip()

    def _get_connections(self, eva_nr: str) -> dict:
        return self.simulation.get_connections(eva_nr)

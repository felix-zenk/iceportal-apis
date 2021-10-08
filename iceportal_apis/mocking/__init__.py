from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from .data import (STATIC_STATUS, STATIC_TRIP, STATIC_CONNECTIONS)


class _Simulation:
    def __init__(self):
        self.simulation_thread = Thread(target=None, daemon=True)
        self._running = False
        self._interval = timedelta(seconds=1)
        self._status = STATIC_STATUS
        self._trip = STATIC_TRIP
        self._connections = STATIC_CONNECTIONS

    def __del__(self):
        try:
            if self._running:
                self.stop()
        except AttributeError:
            pass

    def start(self):
        self.simulation_thread = Thread(target=self._simulate, name=self.__class__.__name__ + "Thread", daemon=True)
        self._running = True
        self.simulation_thread.start()

    def stop(self):
        self._running = False
        # WONT BE NEEDED BECAUSE THREAD IS DAEMON THREAD
        # if self.simulation_thread.is_alive():
        #    self.simulation_thread.join()

    def get_status(self):
        return self._status

    def get_trip(self):
        return self._trip

    def get_connections(self, eva_nr):
        return self._connections[eva_nr]

    def _simulate(self):
        while self._running:
            raise NotImplementedError("This is the base class for simulations. Please use a derived class!")


class StaticSimulation(_Simulation):
    def __init__(self):
        """
        Static simulation of the api
        """
        super(StaticSimulation, self).__init__()

    def get_connections(self, eva_nr):
        return self._connections["8000055_00"]

    def _simulate(self):
        pass


class DynamicSimulation(_Simulation):
    def __init__(self):
        """
        Simulates the behaviour of the onboard api dynamically
        """
        self.data_server = data.DynamicDataServer()
        super(DynamicSimulation, self).__init__()

    def get_connections(self, eva_nr):
        return self._connections["8000055_00"]

    def _refresh_values(self):
        return
        # raise NotImplementedError("The dynamic simulation is not yet implemented!")

    def _simulate(self):
        while self._running:
            start = datetime.now()
            self._refresh_values()
            while (datetime.now() - start) < self._interval:  # removed := for backwards compatibility <3.8
                delta = (datetime.now() - start)
                if not self._running:
                    break
                remaining_time = self._interval - delta
                remaining_milliseconds = remaining_time.microseconds / 1000.0 + 1000 * remaining_time.seconds
                sleep(0.1 if remaining_milliseconds > 100 else remaining_milliseconds / 1000.0)

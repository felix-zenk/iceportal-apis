#!/usr/bin/env python
"""
Note that this module only works on trains from the Deutsche Bahn
Note that this module only works while connected to the on-board network "WIFI@DB" or "WIFIonICE"
"""
from typing import Union, Any, List, Tuple, Dict
from datetime import datetime, timedelta

from onboardapis import Vehicle
from onboardapis.units import kmh
from onboardapis.train import TrainStation as OAStation, ConnectingTrain
from onboardapis.train.de.db import ICEPortal

from .types import (TrainType, WagonClass, InterfaceStatus, Internet)
from .exceptions import (ApiException, NetworkException, NotInFutureException, NotAvailableException,
                         NotOnTrainException, NoneDataException, MissingArgumentError)

import warnings
warnings.warn(
    "This package is no longer maintained in favor of the "
    "'onboardapis' package https://pypi.org/projects/onboardapis."
    "At this point iceportal-apis also is just a wrapper around onboardapis.",
    DeprecationWarning
)


def _ensure_not_none(param: Any) -> Any:
    """
    Tests if an object is not None then returns it or raises an exception
    :param param: The object to test
    :type param: Any
    :return: The same object
    :rtype: Any
    :raises: NotAvailableException
    """
    if param not in {None, ""}:
        return param
    else:
        raise NotAvailableException()


def _convert_to_internet_status(value: str) -> Internet:
    """
    Converts param into an Internet-Status enum
    :param value: The value to convert
    :type value: str
    :return: The enum value
    :rtype: Internet
    """
    if value is None:
        return Internet.UNKNOWN
    return Internet.__members__[value.upper()] if value.upper() in Internet.__members__.keys() else Internet.UNKNOWN


class Station(OAStation):
    def __init__(self, eva_number: str, name: str) -> None:
        super(Station, self).__init__(eva_number, name)

    @property
    def eva_number(self):
        return self.id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Train(Vehicle):
    __oa: ICEPortal

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.__oa = ICEPortal()
        self.__oa.init()

    def __str__(self) -> str:
        return "<%s %s -> %s>" % (self.get_train_type().name, self.get_trip_id(), self.get_next_station().name)

    def get_speed(self) -> float:
        """
        Gets the current speed of the train in kilometers/hour.
        """
        return kmh(ms=self.__oa.speed)

    def get_train_type(self) -> TrainType:
        """
        Gets the train type.
        """
        return TrainType.__members__[self.__oa.type] \
            if self.__oa.type in TrainType.__members__.keys() \
            else TrainType.UNKNOWN

    def get_wagon_class(self) -> WagonClass:
        """
        Gets the wagon class (can be inaccurate for wagons next to another class).
        """
        return (
            WagonClass.__members__[self.__oa.wagon_class]  # type: str
            if self.__oa.wagon_class in WagonClass.__members__.keys()
            else WagonClass.UNKNOWN
        )

    def get_internet_status(self) -> Internet:
        """
        Gets the current internet status / (speed)
        """
        return _convert_to_internet_status(self.__oa.internet_status)

    def get_next_internet_status(self) -> Internet:
        """
        Gets the next internet status / (speed)
        """
        return _convert_to_internet_status(_ensure_not_none(self.__oa.next_internet_status))

    def get_time_until_internet_change(self) -> timedelta:
        """
        Gets the time until the network status changes
        """
        return _ensure_not_none(self.__oa.internet_status_change)

    def has_bap_service(self) -> bool:
        """
        Whether this train offers ordering food from the passengers seat
        :return: Whether this train provides bap service or not
        """
        return self.__oa.has_bap

    def get_latitude(self) -> float:
        """
        Gets the current latitude of the train's position in decimal format.
        """
        return self.__oa.position.latitude

    def get_longitude(self) -> float:
        """
        Gets the current longitude of the train's position in decimal format.
        """
        return self.__oa.position.longitude

    def get_position(self) -> Tuple[float, float]:
        """
        Gets the current position of the train in decimal format.
        """
        return self.__oa.position.latitude, self.__oa.position.longitude

    def get_train_id(self) -> str:
        """
        Gets the unique ID of the train
        """
        return self.__oa.id

    def get_trip_id(self) -> str:
        """
        Gets the ID of the trip
        """
        return self.__oa.line_number

    def get_next_station(self) -> Station:
        """
        Gets the next station
        """
        return Station(self.__oa.current_station.id, self.__oa.current_station.name)

    def get_last_station(self) -> Station:
        """
        Gets the last station.
        """
        station = self.__oa.stations[max(0, self.__oa.stations.index(self.__oa.current_station) - 1)]
        return Station(station.id, station.name)

    def get_final_station(self) -> Station:
        """
        Gets the destination of the train
        """
        return Station(self.__oa.destination.id, self.__oa.destination.name)

    def get_all_stations(self) -> List[Station]:
        """
        Gets all stations for this trip.
        """
        return [
            Station(station.id, station.name) for station in self.__oa.stations
        ]

    def get_arrival_time(self, station: Station) -> datetime:
        """
        Gets the arrival time at a specific station.
        """
        return self.__oa.stations_dict.get(station.eva_number).arrival.actual

    def get_time_until_arrival(self, station: Station) -> timedelta:
        """Gets the time until the arrival at a specific station.
           Returns the difference as a timedelta object.
        """
        return self.get_arrival_time(station) - datetime.now()

    def get_departure_time(self, station: Station) -> datetime:
        """
        Gets the departure time at a specific station.
        """
        return self.__oa.stations_dict.get(station.eva_number).departure.actual

    def get_time_until_departure(self, station: Station) -> timedelta:
        """
        Gets the time until the departure at a specific station.
        Returns the difference as a timedelta object.
        """
        return self.get_departure_time(station) - datetime.now()

    def get_platform(self, station: Station) -> str:
        """
        Gets the trains arrival platform for a specific station
        """
        return self.__oa.stations_dict.get(station.eva_number).platform.actual

    def get_delay_at(self, station: Station) -> timedelta:
        """
        Gets the delay at a station
        """
        return (
            self.__oa.stations_dict.get(station.eva_number).arrival.actual
            - self.__oa.stations_dict.get(station.eva_number).arrival.scheduled
        )

    def get_current_delay(self) -> timedelta:
        """
        Gets the current delay
        """
        return self.__oa.delay

    def is_delayed(self) -> bool:
        """
        Whether the train is delayed
        """
        return self.get_current_delay() > timedelta(seconds=0)

    def get_delay_reasons_at(self, station: Station) -> List[str]:
        """
        Gets the delay reasons for a specific station
        """
        return self.__oa.all_delay_reasons.get(station.eva_number, [])

    def get_current_delay_reasons(self) -> List[str]:
        """
        Gets the current delay reasons
        """
        return self.get_delay_reasons_at(self.get_next_station())

    def get_station_position(self, station: Station) -> Tuple[float, float]:
        """
        Gets the position of a specific station
        """
        pos = self.__oa.stations_dict.get(station.eva_number).position
        return pos.latitude, pos.longitude

    def get_station_distance(self, station: Station) -> float:
        """
        Calculates the distance to a specific station and returns it in meters
        """
        return self.__oa.calculate_distance(self.__oa.stations_dict.get(station.eva_number))

    def get_connections(self, station: Station) -> List[ConnectingTrain]:
        """
        Returns the connecting trains from a specific station
        """
        return self.__oa.stations_dict.get(station.eva_number).connections

    def get_all_connections(self) -> Dict[str, List[ConnectingTrain]]:
        """
        Gets all connections for every available station
        (usually every station except for the first one)
        """
        return {
            station_id: self.__oa.stations_dict.get(station.id).connections
            for station_id, station in self.__oa.stations_dict.items()
        }

    def get_connections_info(self, station) -> List[Dict[str, Union[str, Station, datetime]]]:
        """
        Processes information for connecting trains from station and returns some useful details:\n
        {trainName, finalStation, departure, track}\n
        example: [{'trainName': 'S 5', 'finalStation': Hameln,
        'departure': datetime.datetime(2020, 12, 26, 15, 25), 'track': '1'}, ...]
        """
        return list([
            {
                'trainName': f"{connection.vehicle_type} {connection.line_number}",
                'finalStation': connection.destination,
                'departure': (
                    connection.departure.actual
                    if connection.departure.actual is not None
                    else connection.departure.scheduled
                ),
                'track': (
                    connection.platform.actual
                    if connection.platform.actual is not None
                    else connection.platform.scheduled
                )
            }
            for connection in self.get_connections(station)
        ])

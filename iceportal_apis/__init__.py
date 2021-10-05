#!/usr/bin/env python
"""
Note that this module only works on trains from the Deutsche Bahn
Note that this module only works while connected to the on board network "WIFI@DB" or "WIFIonICE"
"""
from typing import Union, Any
from datetime import datetime, timedelta

from .mocking import TestInterface
from .types import (TrainType, WagonClass, InterfaceStatus, Internet)
from .exceptions import (ApiException, NetworkException, NotInFutureException, NotAvailableException,
                         NotOnTrainException, NoneDataException, MissingArgumentError)

######################################
__author__ = 'Felix Zenk'
__email__ = 'felix.zenk@web.de'
__version__ = '1.1.0'
######################################
URL_STATUS = "https://iceportal.de/api1/rs/status"
URL_TRIP = "https://iceportal.de/api1/rs/tripInfo/trip"
URL_CONNECTIONS = "https://iceportal.de/api1/rs/tripInfo/connection/{}"
URL_POIS = "https://iceportal.de/api1/rs/pois/map/{}/{}/{}/{}"
######################################


def _data_available(param: str) -> bool:
    """
    Tests whether data is available or not
    :param param: The data to test
    :return: Whether it's available or not
    """
    return not (param is None or param == "")


def _ensure_not_none(param: Any) -> Any:
    """
    Tests if an object is not None then returns it or raises an exception
    :param param: The object to test
    :type param: Any
    :return: The same object
    :rtype: Any
    :raises: NotAvailableException
    """
    if param is not None:
        return param
    else:
        raise NotAvailableException()


def _timestamp_to_datetime(timestamp: Union[str, int, float]) -> datetime:
    """
    Converts an int-timestamp with millisecond precision
    :param timestamp: A timestamp that describes elapsed milliseconds
    :type timestamp: Union[str, int, float]
    :return: The datetime object
    :rtype: datetime
    """
    return datetime.fromtimestamp(float(timestamp) / 1000.0)


def _convert_to_internet_status(value: str) -> Internet:
    """
    Converts param into an Internet-Status enum
    :param value: The value to convert
    :type value: str
    :return: The enum value
    :rtype: Internet
    """
    value = value.upper()
    return Internet.HIGH if value == "HIGH" else (
        Internet.WEAK if value == "WEAK" else (
            Internet.UNSTABLE if value == "UNSTABLE" else Internet.UNKNOWN
        )
    )


class Train:
    def __init__(self, auto_refresh: bool = False):
        self._raw_data = TestInterface()
        self._raw_data.set_auto_refresh(auto_refresh=auto_refresh)

    def __str__(self):
        return self.get_train_type().name + " " + self.get_trip_id() + " -> " + self.get_final_station_name()

    def __repr__(self):
        return "<" + str(self) + ">"

    def refresh(self):
        """
        Refreshes all data
        """
        self._raw_data.refresh()

    def get_speed(self):
        """Gets the current speed of the train in kilometers/hour.
        """
        return self._raw_data.status['speed']

    def get_train_type(self):
        """Gets the train type.
        """
        return TrainType.ICE if self._raw_data.status['trainType'].upper() == "ICE" \
            else (TrainType.IC if self._raw_data.status['trainType'].upper() == "IC"
                  else TrainType.UNKNOWN)

    def get_wagon_class(self) -> WagonClass:
        """Gets the wagon class (can be inaccurate for wagons next to another class).
        """
        return WagonClass.FIRST if self._raw_data.status['wagonClass'].upper() == 'FIRST' \
            else (WagonClass.SECOND if self._raw_data.status['wagonClass'].upper() == 'SECOND'
                  else WagonClass.UNKNOWN)

    def get_internet_status(self):
        return _convert_to_internet_status(_ensure_not_none(self._raw_data.status['connectivity']['currentState']))

    def get_next_internet_status(self):
        return _convert_to_internet_status(_ensure_not_none(self._raw_data.status['connectivity']['nextState']))

    def get_time_until_internet_change(self):
        return timedelta(seconds=int(_ensure_not_none(self._raw_data.status['connectivity']['remainingTimeSeconds'])))

    def get_latitude(self):
        """Gets the current latitude of the train's position in decimal format.
        """
        return _ensure_not_none(self._raw_data.status['latitude'])

    def get_longitude(self):
        """Gets the current longitude of the train's position in decimal format.
        """
        return _ensure_not_none(self._raw_data.status['longitude'])

    def get_position(self):
        """Gets the current position of the train in decimal format.
        """
        return self.get_longitude(), self.get_latitude()

    def get_train_id(self):
        """Gets the ID of the train
        """
        return _ensure_not_none(self._raw_data.status['tzn'])

    def get_trip_id(self):
        """Gets the ID of the trip
        """
        return _ensure_not_none(self._raw_data.trip['trip']['vzn'])

    def get_station_eva_number(self, station_name):
        """Gets the evaNr of a specific station.
        """
        return _ensure_not_none(self._raw_data.name_2_eva_nr[station_name])

    def get_next_station_eva_number(self):
        """Gets the evaNr of the next stop.
        """
        return _ensure_not_none(self._raw_data.trip['trip']['stopInfo']['actualNext'])

    def get_last_station_eva_number(self):
        """Gets the evaNr of the last station.
        """
        return _ensure_not_none(self._raw_data.trip['trip']['stopInfo']['actualLast'])

    def get_final_station_eva_number(self):
        """Gets the evaNr of the destination of the train
        """
        return _ensure_not_none(self._raw_data.trip['trip']['stopInfo']['finalStationEvaNr'])

    def get_all_station_eva_numbers(self):
        """Gets the evaNr of all stations for this trip.
        """
        return list(_ensure_not_none(self._raw_data.eva_nr_2_name.keys()))

    def get_station_name(self, eva_nr):
        """Gets the name of a specific station.
        """
        return _ensure_not_none(self._raw_data.eva_nr_2_name[eva_nr])

    def get_next_station_name(self):
        """Gets the name of the next stop.
        """
        return _ensure_not_none(self._raw_data.eva_nr_2_name[self.get_next_station_eva_number()])

    def get_last_station_name(self):
        """
        Gets the name of the last station
        """
        return _ensure_not_none(self._raw_data.eva_nr_2_name[self.get_last_station_eva_number()])

    def get_final_station_name(self):
        """Gets the destination of the train
        """
        return _ensure_not_none(self._raw_data.eva_nr_2_name[self.get_final_station_eva_number()])

    def get_all_station_names(self):
        """
        Gets the names of all stations for this trip.
        """
        return list(self._raw_data.eva_nr_2_name.values())

    def get_arrival_time(self, station_name: str = None, eva_nr: str = None):
        """Gets the arrival time at a specific station.
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return _timestamp_to_datetime(
            _ensure_not_none(self._raw_data.stations[eva_nr]['timetable']['actualArrivalTime']
                             if _data_available(self._raw_data.stations[eva_nr]['timetable']['actualArrivalTime'])
                             else self._raw_data.stations[eva_nr]['timetable']['scheduledArrivalTime']))

    def get_next_arrival_time(self):
        """Gets the arrival time at the next station
        """
        return self.get_arrival_time(eva_nr=self.get_next_station_eva_number())

    def get_time_until_arrival(self, station_name=None, eva_nr=None):
        """Gets the time until the arrival at a specific station.
           Returns the difference as a timedelta object.
        """
        return self.get_arrival_time(station_name=station_name, eva_nr=eva_nr) - datetime.now()

    def get_time_until_next_arrival(self):
        """
        Gets the time until the next stop in minutes
        """
        return self.get_time_until_arrival(eva_nr=self.get_next_station_eva_number())

    def get_departure_time(self, station_name=None, eva_nr=None):
        """
        Gets the departure time at a specific station.
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return _timestamp_to_datetime(
            _ensure_not_none(self._raw_data.stations[eva_nr]['timetable']['actualDepartureTime']
                             if _data_available(self._raw_data.stations[eva_nr]['timetable']['actualDepartureTime'])
                             else self._raw_data.stations[eva_nr]['timetable']['scheduledDepartureTime']
                             ))

    def get_next_departure_time(self):
        """
        Gets the departure time at the next station
        """
        return self.get_departure_time(eva_nr=self.get_next_station_eva_number())

    def get_time_until_departure(self, station_name=None, eva_nr=None):
        """
        Gets the time until the departure at a specific station.
        Returns the difference as a timedelta object.
        """
        return self.get_departure_time(station_name=station_name, eva_nr=eva_nr) - datetime.now()

    def get_time_until_next_departure(self):
        """
        Gets the time until the departure from the next station in minutes
        """
        return self.get_time_until_departure(eva_nr=self.get_next_station_eva_number())

    def get_track(self, station_name=None, eva_nr=None):
        """
        Gets the trains track number for a specific station
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return _ensure_not_none(self._raw_data.stations[eva_nr]['track']['actual']
                                if _data_available(self._raw_data.stations[eva_nr]['track']['actual'])
                                else self._raw_data.stations[eva_nr]['track']['scheduled'])

    def get_next_track(self):
        """
        Gets the track of the next stop
        """
        return self.get_track(eva_nr=self.get_next_station_eva_number())

    def get_delay_at(self, station_name: str = None, eva_nr: str = None):
        """
        Gets the delay in minutes.
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        delay = _ensure_not_none(self._raw_data.stations[eva_nr]['timetable']['arrivalDelay'])
        return 0 if delay == "" else int(delay)

    def get_current_delay(self):
        """
        Gets the delay in minutes.
        """
        return self.get_delay_at(eva_nr=self.get_next_station_eva_number())

    def get_is_delayed(self):
        """
        Whether or not the train is delayed
        """
        return self.get_current_delay() > 0

    def get_delay_reasons_at(self, station_name=None, eva_nr=None):
        """
        Gets the delay reasons for a specific station
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return list([reason['text'] for reason
                     in _ensure_not_none(self._raw_data.stations[eva_nr]['station']['delayReasons'])])

    def get_current_delay_reasons(self):
        """
        Gets the current delay reasons
        """
        return self.get_delay_reasons_at(eva_nr=self.get_next_station_eva_number())

    def get_station_position(self, station_name=None, eva_nr=None):
        """
        Gets the position of a specific station
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return _ensure_not_none(self._raw_data.stations[eva_nr]['station']['geocoordinates']['latitude']), \
            _ensure_not_none(self._raw_data.stations[eva_nr]['station']['geocoordinates']['longitude'])

    def get_station_distance(self, station_name=None, eva_nr=None):
        """
        Calculates the distance to a specific station and returns it in meters
        """
        if not (station_name or eva_nr):
            raise MissingArgumentError()
        elif station_name:
            eva_nr = self._raw_data.name_2_eva_nr[station_name]
        return int(_ensure_not_none(self._raw_data.stations[eva_nr]['info']['distanceFromStart'])) \
            - int(_ensure_not_none(self._raw_data.trip['trip']['actualPosition'])) \
            - int(_ensure_not_none(self._raw_data.trip['trip']['distanceFromLastStop']))

    def get_next_station_distance(self):
        """
        Gets the distance to the next station
        """
        return self.get_station_distance(eva_nr=self.get_next_station_eva_number())

    def get_connections(self, eva_nr: str):
        """Returns the connecting trains from a specific station
        """
        return _ensure_not_none(self._raw_data.connections[eva_nr])

    def get_all_connections(self):
        """
        Gets all connections for every available station
        (usually every station except for the first one)
        """
        return _ensure_not_none(self._raw_data.connections)

    def get_connections_info(self, eva_nr):
        """Processes information on a given dict of connections Returns some useful details: {trainName, finalStation,
        departure, track} example: [{'trainName': 'S 5', 'finalStation': 'Hameln', 'departureTime': datetime.datetime(
        2020, 12, 26, 15, 25), 'track': '1'}, ...]
        """
        return list([{
            'trainName': connection['trainType'] + ' ' + connection['vzn'],
            'finalStation': connection['station']['name'],
            'departure': (connection['timetable']['actualDepartureTime']
                          if not connection['timetable']['actualDepartureTime'] is None
                          else connection['timetable']['scheduledDepartureTime']),
            'track': (connection['track']['actual']
                      if not connection['track']['actual'] is None
                      else connection['timetable']['scheduledDepartureTime'])
        } for connection in self._raw_data.connections[eva_nr]['connections']])

    def get_next_station_connections(self):
        """Gets the connecting trains for the next station
        """
        return self.get_connections_info(self.get_next_station_eva_number())

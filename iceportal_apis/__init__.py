#!/usr/bin/env python
"""
Note that this module only works on trains from the Deutsche Bahn
Note that this module only works while connected to the on board network "WIFI@DB" or "WIFIonICE"
"""
from typing import Union, Any, List, Tuple, Dict
from datetime import datetime, timedelta

from .interfaces import (ApiInterface, TestInterface)
from .mocking import (StaticSimulation, DynamicSimulation)
from .types import (TrainType, WagonClass, InterfaceStatus, Internet)
from .exceptions import (ApiException, NetworkException, NotInFutureException, NotAvailableException,
                         NotOnTrainException, NoneDataException, MissingArgumentError)

######################################
__author__ = 'Felix Zenk'
__email__ = 'felix.zenk@web.de'
__version__ = '1.1.1'
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
    if _data_available(param):
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
    return Internet.__members__[value.upper()] if value.upper() in Internet.__members__.keys() else Internet.UNKNOWN


class Station:
    def __init__(self, eva_number: str, name: str) -> None:
        self.eva_number: str = eva_number
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Train:
    def __init__(self, auto_refresh: bool = False, test_mode: bool = False, dynamic_simulation: bool = False) -> None:
        self._raw_data = TestInterface(DynamicSimulation if dynamic_simulation else StaticSimulation) \
            if test_mode else ApiInterface()
        self._raw_data.set_auto_refresh(auto_refresh=auto_refresh)

    def __del__(self) -> None:
        # Optional, but a clean exit
        try:
            self._raw_data.set_auto_refresh(False)
            if isinstance(self._raw_data, TestInterface):
                self._raw_data.simulation.stop()
        except AttributeError:
            pass

    def __str__(self) -> str:
        return "<"+self.get_train_type().name+" "+self.get_trip_id()+" -> "+self.get_final_station().name+">"

    def __repr__(self) -> str:
        return str(self)

    def refresh(self) -> None:
        """
        Refreshes all data
        """
        self._raw_data.refresh()

    def _station_from_eva_nr(self, eva_nr) -> Station:
        """
        Creates a new Station instance from an eva number
        :param eva_nr: The ave number of the station
        :type eva_nr: str
        :return: A new Station instance
        :rtype: Station
        """
        return Station(eva_number=eva_nr, name=_ensure_not_none(self._raw_data.eva_nr_2_name[eva_nr]))

    def get_speed(self) -> Union[int, str]:
        """
        Gets the current speed of the train in kilometers/hour.
        """
        try:
            return int(_ensure_not_none(self._raw_data.status['speed']))
        except:
            return _ensure_not_none(self._raw_data.status['speed'])

    def get_train_type(self) -> TrainType:
        """
        Gets the train type.
        """
        return TrainType.__members__[self._raw_data.status['trainType'].upper()] \
            if self._raw_data.status['trainType'].upper() in TrainType.__members__.keys() \
            else TrainType.UNKNOWN

    def get_wagon_class(self) -> WagonClass:
        """
        Gets the wagon class (can be inaccurate for wagons next to another class).
        """
        return WagonClass.__members__[self._raw_data.status['wagonClass'].upper()] \
            if self._raw_data.status['wagonClass'].upper() in WagonClass.__members__.keys() \
            else WagonClass.UNKNOWN

    def get_internet_status(self) -> Internet:
        """
        Gets the current internet status / (speed)
        """
        return _convert_to_internet_status(_ensure_not_none(self._raw_data.status['connectivity']['currentState']))

    def get_next_internet_status(self) -> Internet:
        """
        Gets the next internet status / (speed)
        """
        return _convert_to_internet_status(_ensure_not_none(self._raw_data.status['connectivity']['nextState']))

    def get_time_until_internet_change(self) -> timedelta:
        """
        Gets the time until the network status changes
        """
        return timedelta(seconds=int(_ensure_not_none(self._raw_data.status['connectivity']['remainingTimeSeconds'])))

    def has_bap_service(self) -> bool:
        """
        Whether this train offers ordering food from the passengers seat
        :return: Whether this train provides bap service or not
        """
        return _ensure_not_none(self._raw_data.bap["bapServiceStatus"]).upper() == "ACTIVE"

    def get_latitude(self) -> float:
        """
        Gets the current latitude of the train's position in decimal format.
        """
        return _ensure_not_none(self._raw_data.status['latitude'])

    def get_longitude(self) -> float:
        """
        Gets the current longitude of the train's position in decimal format.
        """
        return _ensure_not_none(self._raw_data.status['longitude'])

    def get_position(self) -> Tuple[float, float]:
        """
        Gets the current position of the train in decimal format.
        """
        return self.get_longitude(), self.get_latitude()

    def get_train_id(self) -> str:
        """
        Gets the unique ID of the train
        """
        return _ensure_not_none(self._raw_data.status['tzn'])

    def get_trip_id(self) -> str:
        """
        Gets the ID of the trip
        """
        return _ensure_not_none(self._raw_data.trip['trip']['vzn'])

    def get_next_station(self) -> Station:
        """
        Gets the next station
        """
        return self._station_from_eva_nr(_ensure_not_none(self._raw_data.trip['trip']['stopInfo']['actualNext']))

    def get_last_station(self) -> Station:
        """
        Gets the last station.
        """
        return self._station_from_eva_nr(_ensure_not_none(self._raw_data.trip['trip']['stopInfo']['actualLast']))

    def get_final_station(self) -> Station:
        """
        Gets the destination of the train
        """
        return self._station_from_eva_nr(_ensure_not_none(self._raw_data.trip['trip']['stopInfo']['finalStationEvaNr']))

    def get_all_stations(self) -> List[Station]:
        """
        Gets all stations for this trip.
        """
        return list([self._station_from_eva_nr(eva_nr=eva_nr)
                     for eva_nr in _ensure_not_none(self._raw_data.eva_nr_2_name.keys())])

    def get_arrival_time(self, station: Station) -> datetime:
        """
        Gets the arrival time at a specific station.
        """
        return _timestamp_to_datetime(
            _ensure_not_none(self._raw_data.stations[station.eva_number]['timetable']['actualArrivalTime']
                             if _data_available(
                                self._raw_data.stations[station.eva_number]['timetable']['actualArrivalTime'])
                             else self._raw_data.stations[station.eva_number]['timetable']['scheduledArrivalTime']))

    def get_time_until_arrival(self, station: Station) -> timedelta:
        """Gets the time until the arrival at a specific station.
           Returns the difference as a timedelta object.
        """
        return self.get_arrival_time(station) - datetime.now()

    def get_departure_time(self, station: Station) -> datetime:
        """
        Gets the departure time at a specific station.
        """
        return _timestamp_to_datetime(
            _ensure_not_none(self._raw_data.stations[station.eva_number]['timetable']['actualDepartureTime']
                             if _data_available(
                                self._raw_data.stations[station.eva_number]['timetable']['actualDepartureTime'])
                             else self._raw_data.stations[station.eva_number]['timetable']['scheduledDepartureTime']
                             ))

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
        return _ensure_not_none(self._raw_data.stations[station.eva_number]['track']['actual']
                                if _data_available(
                                    self._raw_data.stations[station.eva_number]['track']['actual'])
                                else self._raw_data.stations[station.eva_number]['track']['scheduled'])

    def get_delay_at(self, station: Station) -> timedelta:
        """
        Gets the delay at a station
        """
        delay = _ensure_not_none(self._raw_data.stations[station.eva_number]['timetable']['arrivalDelay'])
        return timedelta() if delay == "" else timedelta(minutes=int(delay))

    def get_current_delay(self) -> timedelta:
        """
        Gets the current delay
        """
        return self.get_delay_at(self.get_next_station())

    def is_delayed(self) -> bool:
        """
        Whether or not the train is delayed
        """
        return self.get_current_delay() > timedelta()

    def get_delay_reasons_at(self, station: Station) -> List[str]:
        """
        Gets the delay reasons for a specific station
        """
        return list([reason['text'] for reason in self._raw_data.stations[station.eva_number]['delayReasons']]) \
            if self._raw_data.stations[station.eva_number]['delayReasons'] else []

    def get_current_delay_reasons(self) -> List[str]:
        """
        Gets the current delay reasons
        """
        return self.get_delay_reasons_at(self.get_next_station())

    def get_station_position(self, station: Station) -> Tuple[float, float]:
        """
        Gets the position of a specific station
        """
        return _ensure_not_none(self._raw_data.stations[station.eva_number]['station']['geocoordinates']['latitude']), \
            _ensure_not_none(self._raw_data.stations[station.eva_number]['station']['geocoordinates']['longitude'])

    def get_station_distance(self, station: Station) -> int:
        """
        Calculates the distance to a specific station and returns it in meters
        """
        return int(_ensure_not_none(self._raw_data.stations[station.eva_number]['info']['distanceFromStart'])) \
            - int(_ensure_not_none(self._raw_data.trip['trip']['actualPosition'])) \
            - int(_ensure_not_none(self._raw_data.trip['trip']['distanceFromLastStop']))

    def get_connections(self, station: Station) -> List:
        """Returns the connecting trains from a specific station
        """
        return _ensure_not_none(self._raw_data.connections[station.eva_number]['connections'])

    def get_all_connections(self) -> Dict[str, List]:
        """
        Gets all connections for every available station
        (usually every station except for the first one)
        """
        return _ensure_not_none(self._raw_data.connections)

    def get_connections_info(self, station) -> List[Dict[str, Union[str, Station, datetime]]]:
        """
        Processes information for connecting trains from station and returns some useful details:\n
        {trainName, finalStation, departure, track}\n
        example: [{'trainName': 'S 5', 'finalStation': Station(8000148_00, Hameln),
        'departure': datetime.datetime(2020, 12, 26, 15, 25), 'track': '1'}, ...]
        """
        return list([{
            'trainName': connection['trainType'] + ' ' + connection['vzn'],
            'finalStation': Station(connection['station']['evaNr'], connection['station']['name']),
            'departure': _timestamp_to_datetime(connection['timetable']['actualDepartureTime']
                                                if not connection['timetable']['actualDepartureTime'] is None
                                                else connection['timetable']['scheduledDepartureTime']),
            'track': (connection['track']['actual']
                      if not connection['track']['actual'] is None
                      else connection['timetable']['scheduledDepartureTime'])
        } for connection in self.get_connections(station)])

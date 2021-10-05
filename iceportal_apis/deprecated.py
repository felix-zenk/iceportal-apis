#!/usr/bin/env python
"""
Note that this module only works on trains from the Deutsche Bahn
Note that this module only works while connected to the on board network "WIFI@DB" or "WIFIonICE"
"""
import warnings

from requests import get
from datetime import datetime, timedelta
from iceportal_apis.exceptions import *

################################################
__author__ = 'Felix Zenk <..@..>'
__version__ = '1.0.8'
################################################
warnings.warn("This part of the module is deprecated! Use the new functions from the main module.", DeprecationWarning)
################################################
# Exceptions moved
################################################


def convert_time_to_string(timedelta_obj: timedelta, locale: str = "en", no_seconds: bool = False) -> str:
    """
    Converts a timedelta object into a readable string.
       timedelta: timedelta object
       locale: The language code for the returned string
               supported: ('', 'de', 'en', 'fr', 'nl'), standard: 'en'
    """
    if locale.lower() == "de":
        strings_one = ["Tag", "Stunde", "Minute", "Sekunde"]
        strings_many = ["Tage", "Stunden", "Minuten", "Sekunden"]
    elif locale.lower() == "en":
        strings_one = ["day", "hour", "minute", "second"]
        strings_many = ["days", "hours", "minutes", "seconds"]
    elif locale.lower() == "fr":
        strings_one = ["jour", "heure", "minute", "seconde"]
        strings_many = ["jours", "heures", "minutes", "secondes"]
    elif locale.lower() == "nl":
        strings_one = ["dag", "uur", "minuut", "seconde"]
        strings_many = ["dagen", "uur", "minuten", "seconden"]
    else:
        strings_one = ["day", "hour", "minute", "second"]
        strings_many = ["days", "hours", "minutes", "seconds"]

    string_time = ''
    hours = int(timedelta_obj.seconds / 3600)
    minutes = int(timedelta_obj.seconds / 60) - hours * 60
    seconds = timedelta_obj.seconds % 60

    if not timedelta_obj.days == 0:
        if timedelta_obj.days == 1:
            string_time += f' {timedelta_obj.days} {strings_one[0]}'
        else:
            string_time += f' {timedelta_obj.days} {strings_many[0]}'
    if not hours == 0:
        if hours == 1:
            string_time += f' {hours} {strings_one[1]}'
        else:
            string_time += f' {hours} {strings_many[1]}'
    if not minutes == 0:
        if minutes == 1:
            string_time += f' {minutes} {strings_one[2]}'
        else:
            string_time += f' {minutes} {strings_many[2]}'
    if not seconds == 0 and not no_seconds:
        if seconds == 1:
            string_time += f' {seconds} {strings_one[3]}'
        else:
            string_time += f' {seconds} {strings_many[3]}'
    return string_time.strip()


def cut_timestamp(seconds: int) -> int:
    """Cuts the values passed by the api to fit the timestamp format
    """
    return int(str(seconds)[:10])


def calc_distance(position_start: tuple, position_end: tuple) -> float:
    """Calculates the distance between two positions in format (lat, lon)
    """
    from math import pi, sin, cos, sqrt, atan, radians
    f = 1 / 298.257223563
    a = 6378173
    F = radians((position_start[0] + position_end[0]) / 2.0)
    G = radians((position_start[0] - position_end[0]) / 2.0)
    l = radians((position_start[1] - position_end[1]) / 2.0)
    S = sin(G) ** 2 * cos(l) ** 2 + cos(F) ** 2 * sin(l) ** 2
    C = cos(G) ** 2 * cos(l) ** 2 + sin(F) ** 2 * sin(l) ** 2
    w = atan(sqrt(S / C))
    if float(w) == 0.0:
        return 0.0
    D = 2 * w * a
    T = sqrt(S * C) / w
    H_1 = (3 * T - 1) / (2 * C)
    H_2 = (3 * T + 1) / (2 * S)
    return D * (1 + f * H_1 * sin(F) ** 2 * cos(G) ** 2 - f * H_2 * cos(F) ** 2 * sin(G) ** 2)


def autoupdate():
    """Update the module if outdated
    """
    from subprocess import check_output
    from sys import executable
    from os import system
    for row in check_output([executable, "-m", "pip", "list", "--outdated"]).decode('utf-8').split('wheel\r\n')[2:-1]:
        module_info = []
        for p in row.split(' '):
            if not ' ' == p and not '' == p:
                module_info.append(p)
        if 'iceportal-apis' == module_info[0]:
            system(executable + ' -m pip install --upgrade iceportal-apis')


################################################

def request_json(url):
    """Requests data from 'url' and parses it as a dictionary
    """
    try:
        data = get(url)
    except:
        raise NetworkException(url)
    try:
        return data.json()
    except:
        raise NotOnTrainException()


def get_status():
    """Returns the status data.
    """
    return request_json("https://iceportal.de/api1/rs/status")


def get_trip():
    """Returns the trip data.
    """
    return request_json("https://iceportal.de/api1/rs/tripInfo/trip")


def get_all():
    """Pulls data from the api and returns it as dictionaries.
    """
    return get_status(), get_trip()


def get_connecting_trains(evaNr: str) -> dict:
    """Returns the connecting trains from the station <evaNr>
    """
    return request_json("https://iceportal.de/api1/rs/tripInfo/connection/" + evaNr)


################################################

def get_speed(status_call=None):
    """Gets the current speed of the train in kilometers/hour.
    """
    if status_call is not None:
        return status_call['speed']
    return get_status()['speed']


def get_train_type(status_call=None, trip_call=None):
    """Gets the train type.
    """
    if status_call is not None:
        return status_call['trainType']
    if trip_call is not None:
        return trip_call['trip']['trainType']
    return get_status()['trainType']


def get_wagon_class(status_call=None):
    """Gets the wagon class (can be inaccurate for wagons next to another class).
    """
    if status_call is not None:
        return status_call['wagonClass']
    return get_status()['wagonClass']


def get_latitude(status_call=None):
    """Gets the current latitude of the train's position in decimal format.
    """
    if status_call is not None:
        return status_call['latitude']
    return get_status()['latitude']


def get_longitude(status_call=None):
    """Gets the current longitude of the train's position in decimal format.
    """
    if status_call is not None:
        return status_call['longitude']
    return get_status()['longitude']


def get_position(status_call=None):
    """Gets the current position of the train in decimal format.
    """
    if status_call is not None:
        return get_latitude(status_call), get_longitude(status_call)
    return get_latitude(), get_longitude()


def get_train_id(status_call=None):
    """Gets the ID of the train
    """
    if status_call is not None:
        return status_call['tzn']
    return get_status()['tzn']


def get_trip_id(trip_call=None):
    """Gets the ID of the trip
    """
    if trip_call is not None:
        return trip_call['trip']['vzn']
    return get_trip()['trip']['vzn']


def get_station_eva_number(station_name, trip_call=None):
    """Gets the evaNr of a specific station.
    """
    if trip_call is None:
        trip_call = get_trip()
    for stop in trip_call['trip']['stops']:
        if stop['station']['name'] == station_name:
            return stop['station']['evaNr']
    raise NotAvailableException()


def get_next_station_eva_number(trip_call=None):
    """Gets the evaNr of the next stop.
    """
    if trip_call is None:
        trip_call = get_trip()
    return trip_call['trip']['stopInfo']['actualNext']


def get_last_station_eva_number(trip_call=None):
    """Gets the evaNr of a specific station.
    """
    if trip_call is None:
        trip_call = get_trip()
    return trip_call['trip']['stopInfo']['actualLast']


def get_final_station_eva_number(trip_call=None):
    """Gets the evaNr of the destination of the train
    """
    if trip_call is None:
        trip_call = get_trip()
    return trip_call['trip']['stopInfo']['finalStationEvaNr']


def get_all_station_eva_numbers(trip_call=None):
    """Gets the evaNr of all stations for this trip.
    """
    numbers = []
    if trip_call is None:
        trip_call = get_trip()
    for stop in trip_call['trip']['stops']:
        numbers.append(stop['station']['evaNr'])
    if len(numbers) != 0:
        return numbers
    else:
        raise NotAvailableException()


def get_station_name(evaNr, trip_call=None):
    """Gets the name of a specific station.
    """
    if trip_call is None:
        trip_call = get_trip()
    for stop in trip_call['trip']['stops']:
        if stop['station']['evaNr'] == evaNr:
            return stop['station']['name']
    raise NotAvailableException()


def get_next_station_name(trip_call=None):
    """Gets the name of the next stop.
    """
    if trip_call is None:
        trip_call = get_trip()
    for stop in trip_call['trip']['stops']:
        if stop['station']['evaNr'] == trip_call['trip']['stopInfo']['actualNext']:
            return stop['station']['name']
    raise NotAvailableException()


def get_last_station_name(trip_call=None):
    """Gets the name of the last station
    """
    if trip_call is None:
        trip_call = get_trip()
    next_eva_nr = get_next_station_eva_number(trip_call=trip_call)
    for stop in trip_call['trip']['stops']:
        if stop['station']['evaNr'] == next_eva_nr:
            return trip_call['trip']['stops'][trip_call['trip']['stops'].index(stop) - 1]['station']['name']
    raise NotAvailableException()


def get_final_station_name(trip_call=None):
    """Gets the destination of the train
    """
    if trip_call is None:
        trip_call = get_trip()
    return trip_call['trip']['stopInfo']['finalStationName']


def get_all_station_names(trip_call=None):
    """Gets the names of all stations for this trip.
    """
    if trip_call is None:
        trip_call = get_trip()
    names = []
    for stop in trip_call['trip']['stops']:
        names.append(stop['station']['name'])
    if len(names) != 0:
        return names
    else:
        raise NotAvailableException()


def get_arrival_time(station_name=None, evaNr=None, trip_call=None):
    """Gets the arrival time at a specific station.
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()

    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            return datetime.fromtimestamp(cut_timestamp(stop['timetable']['actualArrivalTime']))
    raise NotAvailableException()


def get_next_arrival_time(trip_call=None):
    """Gets the arrival time at the next station
    """
    return get_arrival_time(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_time_until_arrival(station_name=None, evaNr=None, trip_call=None):
    """Gets the time until the arrival at a specific station.
       Returns the difference as a timedelta object.
    """
    if trip_call is None:
        trip_call = get_trip()
    return get_arrival_time(station_name=station_name, evaNr=evaNr, trip_call=trip_call) - datetime.now()


def get_time_until_next_arrival(trip_call=None):
    """Gets the time until the next stop in minutes
    """
    if trip_call is None:
        trip_call = get_trip()
    return get_time_until_arrival(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_departure_time(station_name=None, evaNr=None, trip_call=None):
    """Gets the departure time at a specific station.
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()

    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            return datetime.fromtimestamp(cut_timestamp(stop['timetable']['actualDepartureTime']))
    raise NotAvailableException()


def get_next_departure_time(trip_call=None):
    """Gets the departure time at the next station
    """
    return get_departure_time(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_time_until_departure(station_name=None, evaNr=None, trip_call=None):
    """Gets the time until the departure at a specific station.
       Returns the difference as a timedelta object.
    """
    if trip_call is None:
        trip_call = get_trip()
    return get_departure_time(station_name=station_name, evaNr=evaNr, trip_call=trip_call) - datetime.now()


def get_time_until_next_departure(trip_call=None):
    """Gets the time until the departure from the next station in minutes
    """
    if trip_call is None:
        trip_call = get_trip()
    return get_time_until_departure(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_track(station_name=None, evaNr=None, trip_call=None):
    """Gets the track for a specific station
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()

    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            return int(stop['track']['actual'])
    raise NotAvailableException()


def get_next_track(trip_call=None):
    """Gets the track of the next stop
    """
    return get_track(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_delay(trip_call=None):
    """Gets the delay in minutes.
    """
    if trip_call is None:
        trip_call = get_trip()
    evaNr = get_next_station_eva_number(trip_call=trip_call)
    for stop in trip_call['trip']['stops']:
        if stop['station']['evaNr'] == evaNr:
            if stop['timetable']['arrivalDelay'] == '':
                return 0
            else:
                return int(stop['timetable']['arrivalDelay'])
    raise NotAvailableException()


def get_all_delay_reasons(trip_call=None):
    """Gets all reasons for delays
    """
    if trip_call is None:
        trip_call = get_trip()
    reasons = {}
    for stop in trip_call['trip']['stops']:
        if stop['delayReasons'] is not None:
            this_reasons = []
            for reason in stop['delayReasons']:
                this_reasons.append(reason['text'])
            if len(this_reasons) != 0:
                reasons[stop['station']['evaNr']] = this_reasons
    if len(reasons) != 0:
        return reasons
    raise NoneDataException()  # Train is on time


def get_delay_reasons(trip_call=None):
    """Gets the current delay reasons
    """
    if trip_call is None:
        trip_call = get_trip()
    reasons = []

    for reason in get_delay_reasons_last_station(trip_call=trip_call), get_delay_reasons_for_station(
            evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call):
        if reason:
            for r in reason:
                reasons.append(r)
    if len(reasons) != 0:
        return list(dict.fromkeys(reasons))
    raise NoneDataException()  # Train is on time


def get_delay_reasons_for_station(station_name=None, evaNr=None, trip_call=None):
    """Gets the delay reasons for a specific station
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()

    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            this_reasons = []
            if stop['delayReasons'] is not None:
                for reason in stop['delayReasons']:
                    this_reasons.append(reason['text'])
            return this_reasons
    raise NotAvailableException()


def get_delay_reasons_last_station(trip_call=None):
    """Gets the reasons for the current delay
    """
    return get_delay_reasons_for_station(evaNr=get_last_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_delay_status(trip_call=None):
    """Gets the status of whether the train is delayed or not.
    """
    if get_delay(trip_call=trip_call) > 0:
        return True
    else:
        return False


def get_is_delayed(trip_call=None):
    """Alias for get_delay_status().
    """
    return get_delay_status(trip_call=trip_call)


def get_station_position(station_name=None, evaNr=None, trip_call=None):
    """Gets the position of a specific station
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()

    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            return stop['station']['geocoordinates']['latitude'], stop['station']['geocoordinates']['longitude']


def get_station_distance(station_name=None, evaNr=None, trip_call=None):
    """Calculates the distance to a specific station and returns it in meters
    """
    if trip_call is None:
        trip_call = get_trip()
    if station_name is not None:
        key = 'name'
        value = station_name
    elif evaNr is not None:
        key = 'evaNr'
        value = evaNr
    else:
        raise MissingArgumentError()
    if trip_call is None:
        trip_call = get_trip()
    for stop in trip_call['trip']['stops']:
        if stop['station'][key] == value:
            return stop['info']['distanceFromStart'] - trip_call['trip']['actualPosition'] - trip_call['trip'][
                'distanceFromLastStop']


def get_next_station_distance(trip_call=None):
    """Gets the distance to the next station
    """
    return get_station_distance(evaNr=get_next_station_eva_number(trip_call=trip_call), trip_call=trip_call)


def get_connections(evaNr):
    """Returns the connecting trains from a specific station
    """
    connections = request_json('https://iceportal.de/api1/rs/tripInfo/connection/' + evaNr)
    if connections['requestedEvaNr'] is None:
        raise NotAvailableException()
    else:
        return connections


def get_all_connections():
    """Gets all connections for every available station
    (usually every station except the first one)
    """
    all_connections = []
    for evaNr in get_all_station_eva_numbers():
        try:
            all_connections.append(get_connections(evaNr))
        except NotAvailableException:
            pass


def get_connections_info(connections):
    """Processes information on a given dict of connections Returns some useful details: {trainName, finalStation,
    departure, track} example: [{'trainName': 'S 5', 'finalStation': 'Hameln', 'departureTime': datetime.datetime(
    2020, 12, 26, 15, 25), 'track': '1'}, ...]
    """
    connections_info = []
    for connection in connections['connections']:
        departure = connection['timetable']['actualDepartureTime'] \
            if not connection['timetable']['actualDepartureTime'] is None \
            else connection['timetable']['scheduledDepartureTime']
        track = connection['track']['actual'] \
            if not connection['track']['actual'] == '' \
            else connection['track']['scheduled']
        connections_info.append({'trainName': connection['trainType'] + ' ' + connection['vzn'],
                                 'finalStation': connection['station']['name'],
                                 'departure': datetime.fromtimestamp(cut_timestamp(departure)), 'track': track})
    return connections_info


def get_next_station_connections(trip_call=None):
    """Gets the connecting trains for the next station
    """
    return get_connections_info(get_connections(get_next_station_eva_number(trip_call=trip_call)))

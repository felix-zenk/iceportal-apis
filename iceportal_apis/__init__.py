"""
Note that this module only works on trains from the Deutsche Bahn
Note that this module only works while connected to the on board network "WIFI@DB" or "WIFIonICE"
"""
import requests
from datetime import datetime, timedelta

class NetworkException(Exception):
    """Exception raised when a request fails to fetch data from the api

    Attributes:
        url -- the url that caused the error
        message -- explanation of the error
    """
    def __init__(self, url=None, message='Could not fetch correct data from the server'):
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.url != None:
            return f'Could not fetch correct data from "{self.url}"'
        else:
            return self.message

class NotOnTrainException(Exception):
    """Exception raised when the request returns a website and no json data
    """
    def __init__(self, message='You have to be on a train to use this function'):
        super().__init__(message)

class NotAvailableException(Exception):
    """Exception raised when specific content is not available through the api
    """
    def __init__(self, message='This data is not available on the server'):
        super().__init__(message)

class NotInFutureException(Exception):
    """Exception raised when a timedelta object is negative but only a positive value is allowed
    """
    def __init__(self, message='This event took place in the past, while only future events are allowed'):
        super().__init__(message)

class NoneDataException(Exception):
    """Exception raised when a requested element returns None
    """
    def __init__(self, message='The requested data returned None'):
        super().__init__(message)

class WrongApiException(Exception):
    """Exception raised when a *_call parameter references the wrong api
    """
    def __init__(self, api=None, message='This function requires a call from an other api'):
        self.api=api
        self.message=message
        super().__init__(self.message)

    def __str__(self):
        if self.api != None:
            return f'This function requires data from the "{self.api} API"'
        else:
            return self.message


def convert_time_to_string(timedelta_obj, locale="en"):
    """Converts a timedelta object into a readable string.
       timedelta: timedelta object
       locale: The language code for the returned string
               supported: ('', 'de', 'en', 'fr', 'nl'), standard: 'en'
    """
    now = datetime.now()
    zeroDelta = now-now
    buffer = zeroDelta
    if timedelta_obj < zeroDelta-buffer:
        raise NotInFutureException()
    if locale.lower() == "de":
        strings_one = ["Tag","Stunde","Minute","Sekunde"]
        strings_many = ["Tage","Stunden","Minuten","Sekunden"]
    elif locale.lower() == "en":
        strings_one = ["day","hour","minute","second"]
        strings_many = ["days","hours","minutes","seconds"]
    elif locale.lower() == "fr":
        strings_one = ["jour","heure","minute","seconde"]
        strings_many = ["jours","heures","minutes","secondes"]
    elif locale.lower() == "nl":
        strings_one = ["dag","uur","minuut","seconde"]
        strings_many = ["dagen","uur","minuten","seconden"]
    else:
        strings_one = ["day","hour","minute","second"]
        strings_many = ["days","hours","minutes","seconds"]
    
    string_time = ''
    hours = int(timedelta_obj.seconds/3600)
    minutes = int(timedelta_obj.seconds/60)-hours*60
    seconds = timedelta_obj.seconds%60
    
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
    if not seconds == 0:
        if seconds == 1:
            string_time += f' {seconds} {strings_one[3]}'
        else:
            string_time += f' {seconds} {strings_many[3]}'
    return string_time.strip()

def cut_timestamp(seconds):
    """Cuts the values passed by the api to fit the timestamp format
    """
    return int(str(seconds)[:10])

def request_json(url):
    """Requests data from 'url' and parses it as a dictionary
    """
    try:
        data = requests.get(url)
    except:
        raise NetworkException(url)
    try:
        data_json = data.json()
    except:
        raise NotOnTrainException()
    return data_json

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

def get_speed(status_call=None):
    """Gets the current speed of the train in kilometers/hour.
    """
    if status_call != None:
        return status_call['speed']
    return get_status()['speed']

def get_train_type(status_call=None, trip_call=None):
    """Gets the train type.
    """
    if status_call != None:
        return status_call['trainType']
    if trip_call != None:
        return trip_call['trip']['trainType']
    return get_status()['trainType']

def get_wagon_class(status_call=None):
    """Gets the wagon class (can be inacurate for wagons next to another class).
    """
    if status_call != None:
        return status_call['wagonClass']
    return get_status()['wagonClass']

def get_latitude(status_call=None):
    """Gets the current latitude of the train's position in decimal format.
    """
    if status_call != None:
        return status_call['latitude']
    return get_status()['latitude']

def get_longitude(status_call=None):
    """Gets the current longitude of the train's position in decimal format.
    """
    if status_call != None:
        return status_call['longitude']
    return get_status()['longitude']

def get_position(status_call=None):
    """Gets the current position of the train in decimal format.
    """
    if status_call != None:
        return (get_latitude(status_call), get_longitude(status_call))
    return (get_latitude(), get_longitude())

def get_train_id(status_call=None):
    if status_call != None:
        return status_call['tzn']
    return get_status()['tzn']

def get_trip_id(trip_call=None):
    if trip_call != None:
        return trip_call['trip']['vzn']
    return get_trip()['trip']['vzn']

def get_station_eva_number(station_name, trip_call=None):
    """Gets the evaNr of a specific station.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    for stop in trip['trip']['stops']:
        if stop['station']['name'] == station_name:
            return stop['station']['evaNr']
    raise NotAvailableException()

def get_next_station_eva_number(trip_call=None):
    """Gets the evaNr of the next stop.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return trip['trip']['stopInfo']['actualNext']

def get_last_station_eva_number(trip_call=None):
    """Gets the evaNr of a specific station.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return trip['trip']['stopInfo']['actualLast']

def get_final_station_eva_number(trip_call=None):
    """Gets the evaNr of the destination of the train
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return trip['trip']['stopInfo']['finalStationEvaNr']
    
def get_station_eva_numbers(trip_call=None):
    """Gets the evaNr of all stations for this trip.
    """
    numbers = []
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    for stop in trip['trip']['stops']:
        numbers.append(stop['station']['evaNr'])
    if len(numbers) != 0:
        return numbers
    else:
        raise NotAvailableException()

def get_station_name(evaNr, trip_call=None):
    """Gets the name of a specific station.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    for stop in trip['trip']['stops']:
        if stop['station']['evaNr'] == evaNr:
            return stop['station']['name']
    raise NotAvailableException()

def get_next_station_name(trip_call=None):
    """Gets the name of the next stop.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    for stop in trip['trip']['stops']:
        if stop['station']['evaNr'] == trip['trip']['stopInfo']['actualNext']:
            return stop['station']['name']
    raise NotAvailableException()

def get_last_station_name(trip_call=None):
    """Gets the name of the last station
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    next_eva_nr = get_next_station_eva_number(trip)
    for stop in trip['trip']['stops']:
        if stop['station']['evaNr'] == next_eva_nr:
            return trip['trip']['stops'][trip['trip']['stops'].index(stop)-1]['station']['name']
    raise NotAvailableException()
    
def get_final_station_name(trip_call=None):
    """Gets the destination of the train
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return trip['trip']['stopInfo']['finalStationName']

def get_station_names(trip_call=None):
    """Gets the names of all stations for this trip.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    names = []
    for stop in trip['trip']['stops']:
        names.append(stop['station']['name'])
    if len(names) != 0:
        return names
    else:
        raise NotAvailableException()

def get_arrival_time(station_name=None, evaNr=None, trip_call=None):
    """Gets the arrival time at a specific station.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    if station_name != None:
        key = 'name'
        value = station_name
    elif evaNr != None:
        key = 'evaNr'
        value = evaNr
    else:
        raise TypeError('Missing at least one argument: station_name, evaNr')
    
    for stop in trip['trip']['stops']:
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
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return get_arrival_time(station_name=station_name, evaNr=evaNr, trip_call=trip)-datetime.now()

def get_time_until_next_arrival(trip_call=None):
    """Gets the time until the next stop in minutes
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return get_time_until_arrival(evaNr=get_next_station_eva_number(), trip_call=trip)

def get_departure_time(station_name=None, evaNr=None, trip_call=None):
    """Gets the departure time at a specific station.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    if station_name != None:
        key = 'name'
        value = station_name
    elif evaNr != None:
        key = 'evaNr'
        value = evaNr
    else:
        raise TypeError('Missing at least one argument: station_name, evaNr')
    
    for stop in trip['trip']['stops']:
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
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return get_departure_time(station_name=station_name, evaNr=evaNr, trip_call=trip)-datetime.now()

def get_time_until_next_departure(trip_call=None):
    """Gets the time until the departure from the next station in minutes
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    return get_time_until_departure(evaNr=get_next_station_eva_number(), trip_call=trip)

def get_track(station_name=None, evaNr=None, trip_call=None):
    """Gets the track for a specific station
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    if station_name != None:
        key = 'name'
        value = station_name
    elif evaNr != None:
        key = 'evaNr'
        value = evaNr
    else:
        raise TypeError('Missing at least one argument: station_name, evaNr')
    
    for stop in trip['trip']['stops']:
        if stop['station'][key] == value:
            return int(stop['track']['actual'])
    raise NotAvailableException()

def get_next_track(trip_call=None):
    """Gets the track of the next stop
    """
    return get_track(evaNr=get_next_station_eva_number(), trip_call=trip_call)

def get_delay(trip_call=None):
    """Gets the delay in minutes.
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    evaNr = get_next_station_eva_number(trip)
    for stop in trip['trip']['stops']:
        if stop['station']['evaNr'] == evaNr:
            if stop['timetable']['arrivalDelay'] == '':
                return 0
            else:
                return int(stop['timetable']['arrivalDelay'])
    raise NotAvailableException()

def get_all_delay_reasons(trip_call=None):
    """Gets all reasons for delays
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    reasons = {}
    for stop in trip['trip']['stops']:
        if stop['delayReasons'] != None:
            this_reasons = []
            for reason in stop['delayReasons']:
                this_reasons.append(reason['text'])
            if len(this_reasons) != 0:
                reasons[stop['station']['evaNr']] = this_reasons
    if len(reasons) != 0:
        return reasons
    raise NoneDataException() # Train is on time

def get_delay_reasons(trip_call=None):
    """Gets the current delay reasons
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    reasons = []
    
    reasons.append(get_delay_reasons_last_station())
    reasons.append(get_delay_reasons_for_station(evaNr=get_next_station_eva_number()))
    
    if len(reasons) != 0:
        return list(dict.fromkeys(reasons))
    raise NoneDataException() # Train is on time

def get_delay_reasons_for_station(station_name=None, evaNr=None, trip_call=None):
    """Gets the delay reasons for a specific station
    """
    if trip_call != None:
        trip = trip_call
    else:
        trip = get_trip()
    if station_name != None:
        key = 'name'
        value = station_name
    elif evaNr != None:
        key = 'evaNr'
        value = evaNr
    else:
        raise TypeError('Missing at least one argument: station_name, evaNr')
    
    for stop in trip['trip']['stops']:
        if stop['station'][key] == value:
            this_reasons = []
            if stop['delayReasons'] != None:
                for reason in stop['delayReasons']:
                    this_reasons.append(reason['text'])
            return this_reasons
    raise NotAvailableException()

def get_delay_reasons_last_station(trip_call=None):
    """Gets the reasons for the current delay
    """
    return get_delay_reasons_for_station(evaNr=get_last_station_eva_number())

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
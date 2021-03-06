# iceportal_apis

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.8-yellow)](https://pypi.org/project/iceportal-apis)
[![Supported Python versions](https://img.shields.io/badge/Python-3-blue)](https://pypi.org/project/iceportal-apis)
[![GitHub](https://img.shields.io/badge/license-MIT-green)](LICENSE.txt)

### Description

This module interacts with the onboard APIs of the Deutsche Bahn ICE trains.\
It can do various things from reading the trains velocity to telling you the distance to and the delay at the next station.\
(Explore all functions below at [**`Documentation`**](#documentation)\
This is an inofficial project and neither acknowledged nor supported by `Deutsche Bahn AG`.

> Note, that this module will only work while you are on a train and connected to its WiFi-Hotspot.

For a demo see [`Fahrtinformationen.py`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/Fahrtinformationen.py) or the other files in [`samples`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/)

#

### Installation

* You can directly download the module through the terminal from PyPI
    ```shell
    $ python -m pip install iceportal_apis
    ```
> or download the source files from: [PyPI (web)](https://pypi.org/project/iceportal-apis/#files), 
[GitHub](https://github.com/felix-zenk/iceportal-apis)

#

### Updates

* To update simply *--upgrade* the module through pip.
    ```shell
     $ python -m pip install --upgrade iceportal_apis
    ```
> or see [**`Automatic updates`**](#automatic-updates)-section below
>
> The latest version is: 1.0.8 (12.12.2020)

#

### Changelog

**New in version 1.0.7:**\
\+ Added Changelog\
\+ Added autoupdate() function\
\#  Restructured README

#

**New in version 1.0.8:**\
\# Fixed a flaw with the distance functions\
\# Fixed inconsistent use of status and trip call function parameters\
\# Minor code optimizations\
\# Changed autoupdate() function to support python versions under 3.6\
\+ Added the calc_distance(pos1, pos2) function which calculates the distance between two positions '(lat, lon)' in meters\
\+ Fully implemented the get_station_distance(..) function\
\+ Added the get_next_station_distance() function

#

### License

> **This sofware is distributed under the MIT License, please see [`LICENSE`](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE) for detailed information.**

#

### Documentation

<!---
> ~~This documentation can also be found on [![Documentation link](https://img.shields.io/badge/ReadTheDocs.io-blue)](https://iceportal-apis.readthedocs.io/en/latest/)~~
>
> ReadTheDocs status: [![Documentation Status](https://readthedocs.org/projects/iceportal-apis/badge/?version=latest)](https://iceportal-apis.readthedocs.io/en/latest/?badge=latest)
--->

1. [**Getting data**](#1-getting-data)
    1. [Getting raw data](#11-getting-raw-data)\
        1\. [get_status()](#111-get_status)\
        2\. [get_trip()](#112-get_trip)\
        3\. [get_all()](#113-get_all)\
        4\. [request_json(url)](#114-request_jsonurl)
    2. [Getting processed data](#111-get_status)\
        1\. [get_speed()](#121-get_speedstatus_callnone)\
        2\. [get_train_type()](#122-get_train_typestatus_callnone-trip_callnone)\
        3\. [get_wagon_class()](#123-get_wagon_classstatus_callnone)\
        4\. [get_latitude()](#124-get_latitudestatus_callnone)\
        5\. [get_longitude()](#125-get_longitudestatus_callnone)\
        6\. [get_position()](#126-get_positionstatus_callnone)\
	7\. [get_train_id()](#127-get_train_idstatus_callnone)\
	8\. [get_trip_id()](#128-get_trip_idtrip_callnone)\
        9\. [get_station_eva_number(station_name)](#129-get_station_eva_numbername-trip_callnone)\
        10\. [get_next_station_eva_number()](#1210-get_next_station_eva_numbertrip_callnone)\
        11\. [get_last_station_eva_number()](#1211-get_last_station_eva_numbertrip_callnone)\
	12\. [get_final_station_eva_number()](#1212-get_final_station_eva_numbertrip_callnone)\
        13\. [get_station_eva_numbers()](#1213-get_station_eva_numberstrip_callnone)\
        14\. [get_station_name(evaNr)](#1214-get_station_nameevanr-trip_callnone)\
        15\. [get_next_station_name()](#1215-get_next_station_nametrip_callnone)\
	16\. [get_last_station_name()](#1216-get_last_station_nametrip_callnone)\
	17\. [get_final_station_name()](#1217-get_final_station_nametrip_callnone)\
        18\. [get_station_names()](#1218-get_station_namestrip_callnone)\
        19\. [get_arrival_time(station_name, evaNr)](#1219-get_arrival_timenamenone-evanrnone-trip_callnone)\
	20\. [get_next_arrival_time()](#1220-get_next_arrival_timetrip_callnone)\
	21\. [get_time_until_arrival(station_name, evaNr)](#1221-get_time_until_arrivalnamenone-evanrnone-trip_callnone)\
        22\. [get_time_until_next_arrival()](#1222-get_time_until_next_arrivaltrip_callnone)\
	23\. [get_departure_time(station_name, evaNr)](#1223-get_departure_timenamenone-evanrnone-trip_callnone)\
	24\. [get_next_departure_time()](#1224-get_next_departue_timetrip_callnone)\
	25\. [get_time_until_departure(station_name, evaNr)](#1225-get_time_until_departurenamenone-evanrnone-trip_callnone)\
        26\. [get_time_until_next_departure()](#1226-get_time_until_next_departuretrip_callnone)\
        27\. [get_track(station_name, evaNr)](#1227-get_trackstation_namenone-evanrnone-trip_callnone)\
        28\. [get_next_track()](#1228-get_next_tracktrip_callnone)\
        29\. [get_delay()](#1229-get_delaytrip_callnone)\
        30\. [get_delay_reasons()](#1230-get_delay_reasonstrip_callnone)\
	31\. [get_all_delay_reasons()](#1231-get_delay_reasonstrip_callnone)\
	32\. [get_delay_reasons_for_station(station_name, evaNr)](#1232-get_delay_reasons_for_stationtrip_callnone)\
        33\. [get_delay_reasons_last_station()](#1233-get_delay_reasons_last_stationtrip_callnone)\
        34\. [get_delay_status()](#1234-get_delay_statustrip_callnone)\
        35\. [get_is_delayed()](#1235-get_is_delayedtrip_callnone)\
	36\. [get_station_position(station_name, evaNr)](#1236-get_station_positionstation_namenone-evanrnone-trip_callnone)\
	37\. [get_station_distance(station_name, evaNr)](#1237-get_station_distancestation_namenone-evanrnone-trip_callnone)\
	38\. [get_next_station_distance()](#1238-get_next_station_distancetrip_callnone)
2. [**Processing data**](#2-processing-data)\
    1\. [cut_timestamp(timestamp_int)](#21-cut_timestampseconds)\
    2\. [convert_time_to_string(timedelta_obj)](#22-convert_time_to_stringtimedelta_obj-locale-no_secondsfalse)\
    3\. [calc_distance((start_lat, start_lon), (end_lat, end_lon))](#23-calc_distanceposition_start-position_end)
3. [**Exceptions**](#3-exceptions)\
    1\. [NetworkException(Exception)](#1-networkexceptionexception)\
    2\. [NotOnTrainException(Exception)](#2-notontrainexceptionexception)\
    3\. [NotAvailableException(Exception)](#3-notavailableexceptionexception)\
    4\. [NotInFutureException(Exception)](#4-notinfutureexceptionexception)\
    5\. [NoneDataException(Exception)](#5-nonedataexceptionexception)\
    6\. [*WrongApiException(Exception)*](#6-wrongapiexceptionexception)

### 1. Getting data

### 1.1 Getting raw data

> You can also get the raw data and process it by yourself.
> To build your own fuctions on top of this data see `API documentation` below.

#### 1.1.1 get_status()
>Description: Function for retrieving data from the status API.
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: dict
>
>Calls: request_json

#### 1.1.2 get_trip()
>Description: Function for retrieving data from the trip API
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: dict
>
>Calls: request_json

#### 1.1.3 get_all()
>Description: Gets data from both APIs
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: dict, dict
>
>Calls: request_json

#### 1.1.4 request_json(url)
>Description: Requests data from url and converts it into a python dict
>
>Parameters: url (the url to recieve data from)
>
>Optional parameters: trip_call (dict)
>
>Returns: dict
>
>Calls: requests.get

### 1.2 Getting processed data

`status_call` and `trip_call` are optional parameters.
They can be used to provide the result of an API call to each function. Otherwise the respective function makes a new API call.

##### 1.2.1 get_speed(status_call=None)
>Description: Gets the current speed of the train
>
>Parameters: -
>
>Optional parameters: status_call (dict)
>
>Returns: int
>
>Calls: get_status

#### 1.2.2 get_train_type(status_call=None, trip_call=None)
>Description: Gets the type of train
>
>Parameters: -
>
>Optional parameters: status_call (dict), trip_call (dict)
>
>Returns: String
>
>Calls: get_status, get_trip

#### 1.2.3 get_wagon_class(status_call=None)
>Description: Gets the wagon class (can be inacurate for wagons next to another class)
>
>Parameters: -
>
>Optional parameters: status_call (dict)
>
>Returns: String
>
>Calls: get_status

#### 1.2.4 get_latitude(status_call=None)
>Description: Gets the latitude of the trains position
>
>Parameters: -
>
>Optional parameters: status_call (dict)
>
>Returns: float
>
>Calls: get_status

#### 1.2.5 get_longitude(status_call=None)
>Description: Gets the longitude of the trains position
>
>Parameters: -
>
>Optional parameters: status_call (dict)
>
>Returns: float
>
>Calls: get_status

#### 1.2.6 get_position(status_call=None)
>Description: Gets the trains position
>
>Parameters: -
>
>Optional parameters: status_call (dict)
>
>Returns: (float, float)
>
>Calls: get_latitude, get_longitude

#### 1.2.7 get_train_id(status_call=None)
>Description: Converts a stations name into its evaNr (unsafe: multiple stations in one city)
>
>Parameters: name (String)
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.8 get_trip_id(trip_call=None)
>Description: Converts a stations name into its evaNr (unsafe: multiple stations in one city)
>
>Parameters: name (String)
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.9 get_station_eva_number(name, trip_call=None)
>Description: Converts a stations name into its evaNr (unsafe: multiple stations in one city)
>
>Parameters: name (String)
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.10 get_next_station_eva_number(trip_call=None)
>Description: Gets the evaNr of the next station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.11 get_last_station_eva_number(trip_call=None)
>Description: Gets the evaNr of the last station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.12 get_final_station_eva_number(trip_call=None)
>Description: Gets the evaNr of the final station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.13 get_station_eva_numbers(trip_call=None)
>Description: Gets all evaNrs for this trip
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: list
>
>Calls: get_trip

#### 1.2.14 get_station_name(evaNr, trip_call=None)
>Description: Converts a stations evaNr into its name (safe)
>
>Parameters: evaNr (String)
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.15 get_next_station_name(trip_call=None)
>Description: Gets the name of the next station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.16 get_last_station_name(trip_call=None)
>Description: Gets the name of the last station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip, get_next_station_eva_number

#### 1.2.17 get_final_station_name(trip_call=None)
>Description: Gets the name of the final station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: String
>
>Calls: get_trip

#### 1.2.18 get_station_names(trip_call=None)
>Description: Gets all station names for this trip
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: list
>
>Calls: get_trip

#### 1.2.19 get_arrival_time(name=None, evaNr=None, trip_call=None)
>Description: Gets the time of arrival for a specific station
>
>Parameters: (one needed)
>
>Optional parameters: name (String), evaNr (String), trip_call (dict)
>
>Returns: datetime.datetime
>
>Calls: get_trip, datetime.fromtimestamp, cut_timestamp

#### 1.2.20 get_next_arrival_time(trip_call=None)
>Description: Gets the time of arrival for the next station 
>
>Parameters: -
>
>Returns: datetime.datetime
>
>Calls: get_arrival_time, get_next_station_eva_number

#### 1.2.21 get_time_until_arrival(name=None, evaNr=None, trip_call=None)
>Description: Gets the time until the train arrives at a specific station
>
>Parameters: (one needed)
>
>Optional parameters: name (String), evaNr (String), trip_call (dict)
>
>Returns: datetime.timedelta
>
>Calls: get_arrival_time, datetime.now

#### 1.2.22 get_time_until_next_arrival(trip_call=None)
>Description: Gets the time until the next station in minutes
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: datetime.timedelta
>
>Calls: get_time_until_arrival, get_next_station_eva_number

#### 1.2.23 get_departure_time(name=None, evaNr=None, trip_call=None)
>Description: Gets the time of departure for a specific station
>
>Parameters: (one needed)
>
>Optional parameters: name (String), evaNr (String), trip_call (dict)
>
>Returns: datetime.datetime
>
>Calls: get_trip, datetime.fromtimestamp, cut_timestamp

#### 1.2.24 get_next_departue_time(trip_call=None)
>Description: Gets the time of departure for the next station 
>
>Parameters: -
>
>Returns: datetime.datetime
>
>Calls: get_departure_time, get_next_station_eva_number

#### 1.2.25 get_time_until_departure(name=None, evaNr=None, trip_call=None)
>Description: Gets the time until the train departs at a specific station
>
>Parameters: (one needed)
>
>Optional parameters: name (String), evaNr (String), trip_call (dict)
>
>Returns: datetime.timedelta
>
>Calls: get_departure_time, datetime.now

#### 1.2.26 get_time_until_next_departure(trip_call=None)
>Description: Gets the time until departure from the next station in minutes
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: datetime.timedelta
>
>Calls: get_time_until_departure, get_next_station_eva_number

#### 1.2.27 get_track(station_name=None, evaNr=None, trip_call=None)
>Description: Gets the track on which the train will arrvive for a specific station
>
>Parameters: (one needed)
>
>Optional parameters: station_name (String), evaNr (String), trip_call (dict)
>
>Returns: int
>
>Calls: get_trip

#### 1.2.28 get_next_track(trip_call=None)
>Description: Gets the track on which the train will arrive in the next station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: int
>
>Calls: get_track, get_next_station_eva_number

#### 1.2.29 get_delay(trip_call=None)
>Description: Gets the delay in minutes
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: int
>
>Calls: get_trip, get_next_station_eva_number

#### 1.2.30 get_delay_reasons(trip_call=None)
>Description: Gets the delay reasons for all stations
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: dict
>
>Calls: get_trip

#### 1.2.31 get_delay_reasons(trip_call=None)
>Description: Gets the current delay reasons
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: dict
>
>Calls: get_trip, get_delay_reasons_last_station, get_delay_reasons_for_station, get_next_station_eva_number

#### 1.2.32 get_delay_reasons_for_station(trip_call=None)
>Description: Gets the delay reasons for a specific station
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: list
>
>Calls: get_all_delay_reasons, get_last_station_eva_number

#### 1.2.33 get_delay_reasons_last_station(trip_call=None)
>Description: Gets the reasons for the current delay
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: list
>
>Calls: get_trip, get_all_delay_reasons, get_last_station_eva_number

#### 1.2.34 get_delay_status(trip_call=None)
>Description: Returns whether the train is delayed or not
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: bool
>
>Calls: get_trip, get_delay

#### 1.2.35 get_is_delayed(trip_call=None)
>Description: Alias for get_delay_status
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: bool
>
>Calls: get_trip, get_delay_status

#### 1.2.36 get_station_position(station_name=None, evaNr=None, trip_call=None)
>Description: Gets the position of a specific station
>
>Parameters: (one needed)
>
>Optional parameters: trip_call (dict)
>
>Returns: (float, float)
>
>Calls: get_trip

#### 1.2.37 get_station_distance(station_name=None, evaNr=None, trip_call=None)
>Description: Calculates the distance to a specific station and returns it in meters
>
>Parameters: (one needed)
>
>Optional parameters: trip_call (dict)
>
>Returns: int
>
>Calls: get_trip

#### 1.2.38 get_next_station_distance(trip_call=None)
>Description: Calculates the distance to the next station and returns it in meters
>
>Parameters: -
>
>Optional parameters: trip_call (dict)
>
>Returns: int
>
>Calls: get_trip

### 2. Processing data

#### 2.1 cut_timestamp(seconds)
>Description: The APIs return a timestamp that is not in the right format for datetime functions. This function cuts the timestamp into the right format
>
>Parameters: seconds (int)
>
>Optional parameters: -
>
>Returns: int
>
>Calls: -

#### 2.2 convert_time_to_string(timedelta_obj, locale, no_seconds=False)
>Description: Converts a timedelta object into a string representation, supported locales are "", "en", "de", "fr", "nl". "en" is the standard locale
>
>Parameters: timedelta_obj (datetime.timedelta), locale (String)
>
>Optional parameters: no_seconds (bool)
>
>Returns: String
>
>Calls: datetime.now

#### 2.3 calc_distance(position_start, position_end)
>Description: Calculates the distance between two position tuples.\
>   The function accepts a position like pos = (lat, lon)\
>   A valid call would be something like 'calc_distance((0.0, 0.0), (1.0, 1.0))'
>
>Parameters: position_start ((float, float)), position_end ((float, float))
>
>Optional parameters: -
>
>Returns: float
>
>Calls: -

### 3. Exceptions

#### 1. NetworkException(Exception)
>Description: Exception raised when a request fails to fetch data from the API
>
>Parameters: -
>
>Optional parameters: url (String), message (String)
>
>Raises: Exception
>
#### 2. NotOnTrainException(Exception)
>Description: Exception raised when the request returns a website and no json data -> not on the trains network
>
>Parameters: -
>
>Optional parameters: message (String)
>
>Raises: Exception

#### 3. NotAvailableException(Exception)
>Description: Exception raised when specific content is not available through the API. Example: The train is not delayed -> get_delay_reasons() fails.
>
>Parameters: -
>
>Optional parameters: message (String)
>
>Raises: Exception

#### 4. NotInFutureException(Exception)
>Description: Exception raised when a timedelta object is negative but only a positive value is allowed.
>
>Parameters: -
>
>Optional parameters: message (String)
>
>Raises: Exception

#### 5. NoneDataException(Exception)
>Description: Exception raised when a requested element returns None.
>
>Parameters: -
>
>Optional parameters: message (String)
>
>Raises: Exception

#### 6. WrongApiException(Exception)
>Description: Exception raised when a status/trip_call parameter references the wrong API. Not fully implemented yet!
>
>Parameters: -
>
>Optional parameters: api (String), message (String)
>
>Raises: Exception

#

### Automatic updates

>The `autoupdate` function is only available starting from version 1.0.7 and adds about 10 seconds of delay.
>
>To use auto updates just implement `iceportal_apis.autoupdate()` at some point in your code.
>
>If an update is available changes will be applied at the next program start.
>
>If you want to use this function it is recommended to call `iceportal_apis.autoupdate()` at the end of your program.

#

### Example usage

> This code is also available in the file [`example.py`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/example.py).
```python
# Import iceportal_apis
import iceportal_apis as ipa

# Information related to the next station
def example_next_station():
    """Function for getting the next train station.
       and information on the current status (delay, track, ...)
    """
    print(f'Next stop: "{ipa.get_next_station_name()}" at \
{ipa.get_next_arrival_time()} on platform {ipa.get_next_track()}.')
    print(f'Arrival in {ipa.convert_time_to_string(ipa.get_time_until_next_arrival(), locale="en")}')
    if ipa.get_delay_status():
        print(f'This train is {ipa.get_delay()} min delayed')
        if ipa.get_delay_reasons() != None:
            print(f'Reason: "{ipa.get_delay_reasons_last_station()}"')
    
# Information related to the trains speed
def example_speed():
    """Function for getting the train type and the current speed of the train.
    """
    print(f'This {ipa.get_train_type()} is currently going {ipa.get_speed()}km/h')

    
# Entry
if __name__ == "__main__":
    example_next_station()
    example_speed()
    input() # keep the window opened
```
<br/>

This code makes an API call for every function of `iceportal_apis`. However the module supports handing an API call over to a function as an optional parameter. The function will then work with that call, so that you only need to call the API once.
> This code is also available in the file [`example2.py`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/example2.py).
```python
# same as example.py but calls the api only once

# Import iceportal_apis
import iceportal_apis as ipa

def example_next_station(call):
    """Function for getting the next train station.
       and information on the current status (delay, track, ...)
    """
    print(f'Next stop: "{ipa.get_next_station_name(trip_call=call)}" at \
{ipa.get_next_arrival_time(trip_call=call)} on platform {ipa.get_next_track(trip_call=call)}.')
    print(f'Arrival in {ipa.convert_time_to_string(ipa.get_time_until_next_arrival(trip_call=call), locale="en")}')
    if ipa.get_delay_status(trip_call=call):
        print(f'This train is {ipa.get_delay(trip_call=call)} min delayed')
        if ipa.get_delay_reasons(trip_call=call) != None:
            print(f'Reason: "{ipa.get_delay_reasons_last_station(trip_call=call)}"')
    
# Information related to the trains speed
def example_speed(call):
    """Function for getting the train type and the current speed of the train.
    """
    print(f'This {ipa.get_train_type(status_call=call)} is currently going {ipa.get_speed(status_call=call)}km/h')


# Entry
if __name__ == "__main__":
    # Call the api
    status, trip = ipa.get_all()
    example_next_station(trip)
    example_speed(status)
    input() # keep the window opened
```


#

### API documentation

#### 1. Status API

The Status API is available at [https://iceportal.de/api1/rs/status](https://iceportal.de/api1/rs/status)

Sample response:
```
{
    "connection": true,                         //  true / false
    "servicelevel": "AVAILABLE_SERVICE",        //  ?
    "internet": "HIGH",                         //  HIGH / LOW
    "speed": 185,                               //  int (km/h)
    "gpsStatus": "VALID",                       //  ?
    "tzn": "Tz1191",                            //  Tz.... (train ID)
    "series": "011",                            //  ?
    "latitude": 50.1234567,                     //  float (lat in dec. format)
    "longitude": 10.1234567,                    //  float (lon in dec. format)
    "serverTime": 1603913200000,                //  EPOCH + int
    "wagonClass": "SECOND",                     //  FIRST / SECOND
    "navigationChange": "2020-10-28-04-01-05",  //  YYYY-MM-DD-HH-mm-SS
    "trainType": "ICE"                          //  ICE / IC
}
```

#### 2. Trip API

The Trip API is available at [https://iceportal.de/api1/rs/tripInfo/trip](https://iceportal.de/api1/rs/tripInfo/trip)

Sample Response (**shortened**, only one element in '*stops*' list instead of all stops):
```
{
    "trip": {
        "tripDate": "2020-10-31",       //  date
        "trainType": "ICE",             //  ICE / IC
        "vzn": "881",                   //  trip ID (ICE 881)
        "actualPosition": 159781,       //  distance of the last station from the start
        "distanceFromLastStop": 41632,  //  distance of the train from the last stop
        "totalDistance": 708799,        //  total distance on this trip
        "stopInfo": {
            "scheduledNext": "8000128_00",           //  evaNr
            "actualNext": "8000128_00",              //  evaNr
            "actualLast": "8000152_00",              //  evaNr
            "actualLastStarted": "8000128",          //  evaNr
            "finalStationName": "M\u00fcnchen Hbf",  //  name
            "finalStationEvaNr": "8000261_00"        //  evaNr
        },
        "stops": [
        {
                "station": {
                    "evaNr": "8000115_00",      //  evaNr
                    "name": "Fulda",            //  name
                    "code": null,               //  ?
                    "geocoordinates": {
                        "latitude": 50.554723,  //  float (lat of this station in dec. format)
                        "longitude": 9.683977   //  float (lon of this station in dec. format)
                    }
                },
                "timetable": {
                    "scheduledArrivalTime": 1604159640000,    //  EPOCH + x seconds+ms
                    "actualArrivalTime": 1604159640000,       //  EPOCH + x seconds+ms
                    "showActualArrivalTime": true,            //  -
                    "arrivalDelay": "",                       //  delay in minutes
                    "scheduledDepartureTime": 1604159760000,  //  EPOCH + x seconds+ms
                    "actualDepartureTime": 1604159760000,     //  EPOCH + x seconds+ms
                    "showActualDepartureTime": true,          //  -
                    "departureDelay": ""                      //  delay in minutes
                },
                "track": {
                    "scheduled": "4",  //  The scheduled platform for this train station
                    "actual": "4"      //  The actual platform for this train station
                },
                "info": {
                    "status": 0,                 //  ?
                    "passed": false,             //  false / true (Whether or not the station was already passed)
                    "positionStatus": "future",  //  past / departed / future (see "passed":)
                    "distance": 85974,           //  Distance from last stop
                    "distanceFromStart": 381551  //  Absolute distance travelled
                },
                "delayReasons": [
                    {
                        'code':'38',                                //  delay status code
                        'text':'Technische Störung an der Strecke'  //  delay reason
                    }
                ]
            }
        ]
    },
    "connection": null,               //  ?
    "selectedRoute": {
        "conflictInfo": {
            "status": "NO_CONFLICT",  //  ?
            "text": null              //  ?
        },
        "mobility": null              //  ?
    },
    "active": null                    //  ?
}
```

#### 3. Other APIs

These are other APIs I discovered but didn't investigate in:

3.1. [https://iceportal.de/api1/rs/pois/map/{lat_s}/{lon_s}/{lat_e}/{lon_e}](https://iceportal.de/api1/rs/pois/map/0.000/0.000/1.000/1.000)

3.2. [https://iceportal.de/api1/rs/configs](https://iceportal.de/api1/rs/configs)

3.3. [https://iceportal.de/api1/rs/configs/cities](https://iceportal.de/api1/rs/configs/cities)

#

### Development

> If you would like to develop your own interface you can use sample data from [samples/sample_data_supplier.py](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/sample_data_supplier.py)
Just put the file in your working directory and import it into your project as you would with a normal module.
```python
from sample_data_supplier import get_sample_data_status, get_sample_data_trip, refresh_data
import iceportal_apis as ipa
```
> You have to override the get_status() and get_trip() functions
```python
ipa.get_status = lambda: get_sample_data_status()
ipa.get_trip = lambda: get_sample_data_trip()

# or

ipa.get_status = get_sample_data_status
ipa.get_trip = get_sample_data_trip
```
> Update the recorded timestamps to the current time
```
refresh_data()
```
> After that you can develop and test as if you were on a train.

Example:
```python
from sample_data_supplier import get_sample_data_status, get_sample_data_trip
import iceportal_apis as ipa

ipa.get_status = lambda: get_sample_data_status()
ipa.get_trip = lambda: get_sample_data_trip()

print(ipa.get_speed())
```

### Further simulating

> If you want to simulate a complete trip the [samples](https://github.com/felix-zenk/iceportal-apis/blob/main/samples) serve as a solid base.

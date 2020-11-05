# iceportal_apis
### Description
This module functions as an endpoint for interacting with the onboard APIs of the Deutsche Bahn ICE and IC trains.
This is an inofficial project and not acknowledged nor supported by `Deutsche Bahn AG`.
> Note, that this module will only work while you are on a train and connected to its WiFi-Hotspot.

#
### Installation
* Available on PyPI
    ```shell
    $ python -m pip install iceportal_apis
    ```
* Or directly download this module from: [Direct download (PyPI)](https://pypi.org/project/iceportal-apis/#files)
#
### Updates
* To update simply upgrade the module through pip.
    ```shell
     $ python -m pip install --upgrade iceportal_apis
    ```
* The newest version is: 1.0.1

#
### License
* This sofware is distributed under the MIT License, please see `LICENSE` for detailed information.

#
### Documentation
1. Getting data
    1. Getting raw data\
        1\. get_status()\
        2. get_trip()\
        3. get_all()\
        4. request_json(url)
    2. Getting processed data\
        1\. get_speed()\
        2. get_train_type()\
        3. get_wagon_class()\
        4. get_latitude()\
        5. get_longitude()\
        6. get_position()\
        7. get_station_eva_number(name)\
        8. get_next_station_eva_number()\
        9. get_last_station_eva_number()\
        10. get_station_eva_numbers()\
        11. get_station_name(evaNr)\
        12. get_next_station_name()\
        13. get_station_names()
        14. get_actual_arrival_time(name, evaNr)\
        15. get_next_arrival_time()\
        16. get_actual_time_until_arrival(name, evaNr)\
        17. get_time_until_arrival(name, evaNr)\
        18. get_actual_time_until_next_arrival()\
        19. get_time_until_next_arrival()\
        20. get_actual_track(station, evaNr)\
        21. get_track(station, evaNr)\
        22. get_next_track()\
        23. get_delay()\
        24. get_delay_reasons()\
        25. get_delay_reasons_last_station()\
        26. get_delay_reason()\
        27. get_delay_status()\
        28. get_is_delayed()
2. Processing data\
    1\. cut_timestamp(seconds)\
    2. convert_time_to_string(timedelta_obj, locale)
3. Exceptions\
    1\. NetworkException(Exception)\
    2. NotOnTrainException(Exception)\
    3. NotAvailableException(Exception)\
    4. NotInFutureException(Exception)\
    5. NoneDataException(Exception)\
    6. WrongApiException(Exception)

### 1. Getting data
### 1.1 Getting raw data
#### 1.1.1 get_status()
>Description: Function for retrieving data from the status API.

>Parameters: -

>Returns: dict

>Calls: request_json

#### 1.1.2 get_trip()
>Description: Function for retrieving data from the trip API

>Parameters: -

>Returns: dict

>Calls: request_json

#### 1.1.3 get_all()
>Description: Gets data from both APIs

>Parameters: -

>Returns: dict, dict

>Calls: request_json

#### 1.1.4 request_json(url)
>Description: Requests data from url and converts it into a python dict

>Parameters: url (the url to recieve data from)

>Returns: dict

>Calls: requests.get

### 1.2 Getting processed data

`status_call` and `trip_call` are optional parameters.
They can be used to provide the result of an API call to each function. Otherwise the respective function makes a new API call.

##### 1.2.1 get_speed(status_call=None)
>Description: Gets the current speed of the train

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: int

>Calls: get_status

#### 1.2.2 get_train_type(status_call=None)
>Description: Gets the type of train

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: String ("ICE"/"IC")

>Calls: get_status

#### 1.2.3 get_wagon_class(status_call=None)
>Description: Gets the wagon class (can be inacurate for wagons next to another class)

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: String ("FIRST"/"SECOND")

>Calls: get_status

#### 1.2.4 get_latitude(status_call=None)
>Description: Gets the latitude of the trains position

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: float

>Calls: get_status

#### 1.2.5 get_longitude(status_call=None)
>Description: Gets the longitude of the trains position

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: float

>Calls: get_status

#### 1.2.6 get_position(status_call=None)
>Description: Gets the trains position

>Parameters: -

>Optional parameters: status_call (dict)

>Returns: (float, float)

>Calls: get_latitude, get_longitude

#### 1.2.7 get_station_eva_number(name, trip_call=None)
>Description: Converts a stations name into its evaNr (unsafe: multiple stations in one city)

>Parameters: name (String)

>Optional parameters: trip_call (dict)

>Returns: String

>Calls: get_trip

#### 1.2.8 get_next_station_eva_number(trip_call=None)
>Description: Gets the evaNr of the next station

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: String

>Calls: get_trip

#### 1.2.9 get_last_station_eva_number(trip_call=None)
>Description: Gets the evaNr of the last station

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: String

>Calls: get_trip, get_next_station_eva_number

#### 1.2.10 get_station_eva_numbers(trip_call=None)
>Description: Gets all evaNrs for this trip

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: list

>Calls: get_trip

#### 1.2.11 get_station_name(evaNr, trip_call=None)
>Description: Converts a stations evaNr into its name (safe)

>Parameters: evaNr (String)

>Optional parameters: trip_call (dict)

>Returns: String

>Calls: get_trip

#### 1.2.12 get_next_station_name(trip_call=None)
>Description: Gets the name of the next station

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: String

>Calls: get_trip

#### 1.2.13 get_station_names(trip_call=None)
>Description: Gets all station names for this trip

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: list

>Calls: get_trip

#### 1.2.14 get_actual_arrival_time(name=None, evaNr=None, trip_call=None)
>Description: Gets the time of arrival for a specific station

>Parameters: (one needed)

>Optional parameters: name (String), evaNr (String), trip_call (dict)

>Returns: datetime.datetime

>Calls: get_trip, datetime.fromtimestamp, cut_timestamp

#### 1.2.15 get_next_arrival_time(trip_call=None)
>Description: Gets the time of arrival for the next station 

>Parameters: -

>Returns: datetime.datetime

>Calls: get_actual_arrival_time, get_next_station_eva_number

#### 1.2.16 get_actual_time_until_arrival(name=None, evaNr=None, trip_call=None)
>Description: Gets the time until the train arrives at a specific station

>Parameters: (one needed)

>Optional parameters: name (String), evaNr (String), trip_call (dict)

>Returns: datetime.timedelta

>Calls: get_actual_arrival_time, datetime.now

#### 1.2.17 get_time_until_arrival(name=None, evaNr=None, trip_call=None)
>Description: Alias for get_actual_time_until_arrival()

>Parameters: (one needed)

>Optional parameters: name (String), evaNr (String), trip_call (dict)

>Returns: datetime.timedelta

>Calls: get_actual_time_until_arrival

#### 1.2.18 get_actual_time_until_next_arrival(trip_call=None)
>Description: Gets the time until the next station in minutes

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: datetime.timedelta

>Calls: get_actual_time_until_arrival, get_next_station_eva_number

#### 1.2.19 get_time_until_next_arrival(trip_call=None)
>Description: Alias for get_actual_time_until_next_arrival

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: datetime.timedelta

>Calls: get_actual_time_until_next_arrival

#### 1.2.20 get_actual_track(station_name=None, evaNr=None, trip_call=None)
>Description: Gets the track on which the train will arrvive for a specific station

>Parameters: (one needed)

>Optional parameters: station_name (String), evaNr (String), trip_call (dict)

>Returns: int

>Calls: get_trip, 

#### 1.2.21 get_track(station=None, evaNr=None, trip_call=None)
>Description: Alias for get_actual_track()

>Parameters: (one needed)

>Optional parameters: station_name (String), evaNr (String), trip_call (dict)

>Returns: int

>Calls: get_actual_track

#### 1.2.22 get_next_track(trip_call=None)
>Description: Gets the track on which the train will arrive in the next station

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: int

>Calls: get_actual_track, get_next_station_eva_number

#### 1.2.23 get_delay(trip_call=None)
>Description: Gets the delay in minutes

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: int

>Calls: get_trip, get_next_station_eva_number

#### 1.2.24 get_delay_reasons(trip_call=None)
>Description: Gets all reasons for delays

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: dict

>Calls: get_trip

#### 1.2.25 get_delay_reasons_last_station(trip_call=None)
>Description: Gets the reasons for the current delay

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: list

>Calls: get_delay_reasons, get_last_station_eva_number

#### 1.2.26 get_delay_reason(trip_call=None)
>Description: Alias for get_delay_reason_last_station

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: list

>Calls: get_delay_reason_last_station

#### 1.2.27 get_delay_status(trip_call=None)
>Description: Returns whether the train is delayed or not

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: bool

>Calls: get_delay

#### 1.2.28 get_is_delayed(trip_call=None)
>Description: Alias for get_delay_status

>Parameters: -

>Optional parameters: trip_call (dict)

>Returns: bool

>Calls: get_delay_status

### 2. Processing data
#### 2.1 cut_timestamp(seconds)
>Description: The APIs return a timestamp that is not in the right format for datetime functions. This function cuts the timestamp into the right format

>Parameters: seconds (int)

>Returns: int

>Calls: -

#### 2.2 convert_time_to_string(timedelta_obj, locale)
>Description: Converts a timedelta object into a string representation, supported locales are "", "en", "de", "fr", "nl". "en" is the standard locale

>Parameters: timedelta_obj (datetime.timedelta), locale (String)

>Returns: String

>Calls: datetime.now

### 3. Exceptions
#### 1. Work in progress ...

#
### Example usage
> This code is also available in the file [`example.py`](https://github.com/felix-zenk/python-iceportal_apis/blob/main/samples/example.py).
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
            print(f'Reason: "{ipa.get_delay_reason_last_station()}"')
    
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
> This code is also available in the file [`example2.py`](https://github.com/felix-zenk/python-iceportal_apis/blob/main/samples/example2.py).
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
            print(f'Reason: "{ipa.get_delay_reason_last_station(trip_call=call)}"')
    
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
    input()
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
        "actualPosition": 159781,       //  distance from the start
        "distanceFromLastStop": 41632,  //  distance from the last stop
        "totalDistance": 708799,        //  total distance
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
                    "scheduledArrivalTime": 1604159640000,    //  EPOCH + x seconds
                    "actualArrivalTime": 1604159640000,       //
                    "showActualArrivalTime": true,            //  -
                    "arrivalDelay": "",                       //  delay in minutes
                    "scheduledDepartureTime": 1604159760000,  //
                    "actualDepartureTime": 1604159760000,     //
                    "showActualDepartureTime": true,          //  -
                    "departureDelay": ""                      //  delay in minutes
                },
                "track": {
                    "scheduled": "4",  //  The scheduled platform in this train station
                    "actual": "4"      //  The actual platform in this train station
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

3.1. [https://iceportal.de/api1/rs/pois/map](https://iceportal.de/api1/rs/pois/map)

3.2. [https://iceportal.de/api1/rs/configs](https://iceportal.de/api1/rs/configs)

3.3. [https://iceportal.de/api1/rs/configs/cities](https://iceportal.de/api1/rs/configs/cities)
#
### Development
> If you would like to develop your own interface you can use sample data from [samples/sample_data_supplier.py](https://github.com/felix-zenk/python-iceportal_apis/blob/main/samples/sample_data_supplier.py)
Just put the file in your working directory and import it into your project as you would with a normal module.
```python
from sample_data_supplier import get_sample_data_status, get_sample_data_trip
import iceportal_apis as ipa
```
> You have to override the get_status() and get_trip() functions
```python
ipa.get_status = lambda: get_sample_data_status()
ipa.get_trip = lambda: get_sample_data_trip()
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

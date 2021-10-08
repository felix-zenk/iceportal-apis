# iceportal_apis

[![PyPI version](https://img.shields.io/badge/pypi-v1.1.0-yellow)](https://pypi.org/project/iceportal-apis)
[![Supported Python versions](https://img.shields.io/badge/Python-3-blue)](https://pypi.org/project/iceportal-apis)
[![GitHub](https://img.shields.io/badge/license-MIT-green)](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE)

### Description
This module interacts with the onboard APIs of the Deutsche Bahn ICE trains.\
It can do various things from reading the trains' velocity to telling you the distance to and the delay at the next station.\
( Explore all functions below at [`Documentation`](https://github.com/felix-zenk/iceportal-apis#documentation) )\
This is an unofficial project and not supported by [`Deutsche Bahn AG`](https://www.deutschebahn.com/de/konzern).
> Note, that this module will only work correctly while you are on a train and connected to its WiFi-Hotspot.\
> However a basic simulation for offline research is also included in this module

#

### Installation
* Available on PyPI
    ```shell
    $ python -m pip install iceportal_apis
    ```
  for the newest (unstable) version install the module from GitHub
    ```shell
    $ python -m pip install git+https://github.com/felix-zenk/iceportal-apis.git
    ```

> Or download the source files from: [PyPI (web)](https://pypi.org/project/iceportal-apis/#files), 
[GitHub](https://github.com/felix-zenk/iceportal-apis)
> and install via setup.py
>
> The latest version is: v1.1.0 (09.10.2021)

#

### Usage
> Example code is available in the file [`example.py`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/example.py) and other files in [`samples`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples).
>
> The basic usage consists of requesting new data from the api, then processing it with the modules functions.

```python
import iceportal_apis as ipa

train = ipa.Train()

while True:
    # Request new data from the api
    train.refresh()
    
    # Process data
    print(train.get_train_type().name)
    next_station = train.get_next_station()

    . . .
```

> For GUI applications you can also specify automatic api polling

```python
train = ipa.Train(auto_refresh=True)
```

#

### License
> **This software is distributed under the MIT License, please see [`LICENSE`](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE) for detailed information.**

#

### <div id="documentation">Documentation</div>

1. **Work**
    1. in\
        1\. progress



#

### <div id="api">API documentation</div>

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

#### 3. Connections API

```python
{
        "connections": [
            {
                "trainType": "S",
                "vzn": "3",
                "trainNumber": "38334",
                "station": {
                    "evaNr": "8000376_00",
                    "name": "Germersheim",
                    "code": None,
                    "geocoordinates": {
                        "latitude": 49.225402,
                        "longitude": 8.365282
                    }
                },
                "timetable": {
                    "scheduledArrivalTime": None,
                    "actualArrivalTime": None,
                    "showActualArrivalTime": None,
                    "arrivalDelay": '',
                    "scheduledDepartureTime": 1611232980000,
                    "actualDepartureTime": 1611232980000,
                    "showActualDepartureTime": True,
                    "departureDelay": ''
                },
                "track": {
                    "scheduled": "3b",
                    "actual": "3b"
                },
                "info": {
                    "status": 0,
                    "passed": False,
                    "positionStatus": None,
                    "distance": 0,
                    "distanceFromStart": 0
                },
                "stops": [
                    {"station": {"evaNr": "8000055_00", "name": "Bruchsal", "code": None, "geocoordinates": {"latitude": 49.124622, "longitude": 8.589649}}, "timetable": {"scheduledArrivalTime": None, "actualArrivalTime": None, "showActualArrivalTime": None, "arrivalDelay": '', "scheduledDepartureTime": 1611232980000, "actualDepartureTime": 1611232980000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "3b", "actual": "3b"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005931_00", "name": "Ubstadt-Weiher", "code": None, "geocoordinates": {"latitude": 49.167021, "longitude": 8.623335}}, "timetable": {"scheduledArrivalTime": 1611233160000, "actualArrivalTime": 1611233220000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005933_00", "name": "Stettfeld-Weiher", "code": None, "geocoordinates": {"latitude": 49.183625, "longitude": 8.636928}}, "timetable": {"scheduledArrivalTime": 1611233340000, "actualArrivalTime": 1611233340000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8003533_00", "name": "Bad Schönborn Süd", "code": None, "geocoordinates": {"latitude": 49.200001, "longitude": 8.641924}}, "timetable": {"scheduledArrivalTime": 1611233460000, "actualArrivalTime": 1611233460000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8004032_00", "name": "Bad Schönborn-Kronau", "code": None, "geocoordinates": {"latitude": 49.219345, "longitude": 8.646821}}, "timetable": {"scheduledArrivalTime": 1611233580000, "actualArrivalTime": 1611233640000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005181_00", "name": "Rot-Malsch", "code": None, "geocoordinates": {"latitude": 49.243385, "longitude": 8.65221}}, "timetable": {"scheduledArrivalTime": 1611233760000, "actualArrivalTime": 1611233760000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8006421_00", "name": "Wiesloch-Walldorf", "code": None, "geocoordinates": {"latitude": 49.291353, "longitude": 8.664146}}, "timetable": {"scheduledArrivalTime": 1611234000000, "actualArrivalTime": 1611234000000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005648_00", "name": "St Ilgen-Sandhausen", "code": None, "geocoordinates": {"latitude": 49.341268, "longitude": 8.668715}}, "timetable": {"scheduledArrivalTime": 1611234240000, "actualArrivalTime": 1611234240000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8002686_00", "name": "Heidelberg-Kirchheim/Rohrbach", "code": None, "geocoordinates": {"latitude": 49.379389, "longitude": 8.675383}}, "timetable": {"scheduledArrivalTime": 1611234420000, "actualArrivalTime": 1611234480000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000156_00", "name": "Heidelberg Hbf", "code": None, "geocoordinates": {"latitude": 49.403567, "longitude": 8.675442}}, "timetable": {"scheduledArrivalTime": 1611234720000, "actualArrivalTime": 1611234720000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8002687_00", "name": "Heidelberg-Pfaffengrund/Wieblingen", "code": None, "geocoordinates": {"latitude": 49.411929, "longitude": 8.64157}}, "timetable": {"scheduledArrivalTime": 1611234960000, "actualArrivalTime": 1611234960000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8003842_00", "name": "Mannheim-Friedrichsfeld Süd", "code": None, "geocoordinates": {"latitude": 49.438144, "longitude": 8.572382}}, "timetable": {"scheduledArrivalTime": 1611235200000, "actualArrivalTime": 1611235200000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000244_00", "name": "Mannheim Hbf", "code": None, "geocoordinates": {"latitude": 49.479354, "longitude": 8.468921}}, "timetable": {"scheduledArrivalTime": 1611235740000, "actualArrivalTime": 1611235740000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8003759_00", "name": "Ludwigshafen (Rhein) Mitte", "code": None, "geocoordinates": {"latitude": 49.479005, "longitude": 8.452152}}, "timetable": {"scheduledArrivalTime": 1611235980000, "actualArrivalTime": 1611235980000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000236_00", "name": "Ludwigshafen (Rh) Hbf", "code": None, "geocoordinates": {"latitude": 49.477987, "longitude": 8.433402}}, "timetable": {"scheduledArrivalTime": 1611236100000, "actualArrivalTime": 1611236160000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8003687_00", "name": "Limburgerhof", "code": None, "geocoordinates": {"latitude": 49.424273, "longitude": 8.390747}}, "timetable": {"scheduledArrivalTime": 1611236460000, "actualArrivalTime": 1611236580000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "3", "actual": "3"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000326_00", "name": "Schifferstadt", "code": None, "geocoordinates": {"latitude": 49.39291, "longitude": 8.364945}}, "timetable": {"scheduledArrivalTime": 1611236760000, "actualArrivalTime": 1611236820000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "3", "actual": "3"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005345_00", "name": "Schifferstadt Süd", "code": None, "geocoordinates": {"latitude": 49.374089, "longitude": 8.377314}}, "timetable": {"scheduledArrivalTime": 1611237000000, "actualArrivalTime": 1611237000000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005626_00", "name": "Speyer Nord-West", "code": None, "geocoordinates": {"latitude": 49.333592, "longitude": 8.419263}}, "timetable": {"scheduledArrivalTime": 1611237240000, "actualArrivalTime": 1611237240000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8005628_00", "name": "Speyer Hbf", "code": None, "geocoordinates": {"latitude": 49.324119, "longitude": 8.427949}}, "timetable": {"scheduledArrivalTime": 1611237360000, "actualArrivalTime": 1611237360000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "3", "actual": "3"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000894_00", "name": "Berghausen (Pfalz)", "code": None, "geocoordinates": {"latitude": 49.295449, "longitude": 8.406173}}, "timetable": {"scheduledArrivalTime": 1611237600000, "actualArrivalTime": 1611237600000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8002704_00", "name": "Heiligenstein (Pfalz)", "code": None, "geocoordinates": {"latitude": 49.28566, "longitude": 8.393726}}, "timetable": {"scheduledArrivalTime": 1611237720000, "actualArrivalTime": 1611237720000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8003702_00", "name": "Lingenfeld", "code": None, "geocoordinates": {"latitude": 49.252584, "longitude": 8.349523}}, "timetable": {"scheduledArrivalTime": 1611237900000, "actualArrivalTime": 1611237900000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8000376_00", "name": "Germersheim", "code": None, "geocoordinates": {"latitude": 49.225402, "longitude": 8.365282}}, "timetable": {"scheduledArrivalTime": 1611238140000, "actualArrivalTime": 1611238260000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "5", "actual": "5"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None}
                ]
            },
            {
                "trainType": "S",
                "vzn": "32",
                "trainNumber": "85073",
                "station": {
                    "evaNr": "8007145_00",
                    "name": "Menzingen (Baden)",
                    "code": None,
                    "geocoordinates": {
                        "latitude": 49.136233,
                        "longitude": 8.775067
                    }
                },
                "timetable": {
                    "scheduledArrivalTime": None,
                    "actualArrivalTime": None,
                    "showActualArrivalTime": None,
                    "arrivalDelay": '',
                    "scheduledDepartureTime": 1611234720000,
                    "actualDepartureTime": 1611234840000,
                    "showActualDepartureTime": True,
                    "departureDelay": "+2"
                },
                "track": {
                    "scheduled": "3a",
                    "actual": "3a"
                },
                "info": {
                    "status": 0,
                    "passed": False,
                    "positionStatus": None,
                    "distance": 0,
                    "distanceFromStart": 0
                },
                "stops": [
                    {"station": {"evaNr": "8000055_00", "name": "Bruchsal", "code": None, "geocoordinates": {"latitude": 49.124622, "longitude": 8.589649}}, "timetable": {"scheduledArrivalTime": None, "actualArrivalTime": None, "showActualArrivalTime": None, "arrivalDelay": '', "scheduledDepartureTime": 1611234720000, "actualDepartureTime": 1611234840000, "showActualDepartureTime": True, "departureDelay": "+2"}, "track": {"scheduled": "3a", "actual": "3a"}, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8085001_00", "name": "Bruchsal Schloßgarten", "code": None, "geocoordinates": {"latitude": 49.131438, "longitude": 8.59406}}, "timetable": {"scheduledArrivalTime": 1611234780000, "actualArrivalTime": 1611234900000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8085002_00", "name": "Bruchsal Stegwiesen", "code": None, "geocoordinates": {"latitude": 49.136435, "longitude": 8.598199}}, "timetable": {"scheduledArrivalTime": 1611234900000, "actualArrivalTime": 1611235020000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007133_00", "name": "Ubstadt Ort", "code": None, "geocoordinates": {"latitude": 49.156748, "longitude": 8.625553}}, "timetable": {"scheduledArrivalTime": 1611235080000, "actualArrivalTime": 1611235200000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8085003_00", "name": "Ubstadt Salzbrunnenstr", "code": None, "geocoordinates": {"latitude": 49.15519, "longitude": 8.633025}}, "timetable": {"scheduledArrivalTime": 1611235200000, "actualArrivalTime": 1611235260000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8079149_00", "name": "Unteröwisheim M.-Luther-Str.", "code": None, "geocoordinates": {"latitude": 49.146484, "longitude": 8.66202}}, "timetable": {"scheduledArrivalTime": 1611235380000, "actualArrivalTime": 1611235560000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007140_00", "name": "Unteröwisheim Bf", "code": None, "geocoordinates": {"latitude": 49.146342, "longitude": 8.668986}}, "timetable": {"scheduledArrivalTime": 1611235440000, "actualArrivalTime": 1611235620000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007141_00", "name": "Oberöwisheim", "code": None, "geocoordinates": {"latitude": 49.14006, "longitude": 8.686232}}, "timetable": {"scheduledArrivalTime": 1611235560000, "actualArrivalTime": 1611235740000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007142_00", "name": "Münzesheim", "code": None, "geocoordinates": {"latitude": 49.12608, "longitude": 8.716007}}, "timetable": {"scheduledArrivalTime": 1611235740000, "actualArrivalTime": 1611235920000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007146_00", "name": "Münzesheim Ost", "code": None, "geocoordinates": {"latitude": 49.121492, "longitude": 8.726215}}, "timetable": {"scheduledArrivalTime": 1611235860000, "actualArrivalTime": 1611236100000, "showActualArrivalTime": True, "arrivalDelay": "+4", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007143_00", "name": "Gochsheim (Baden)", "code": None, "geocoordinates": {"latitude": 49.109411, "longitude": 8.744695}}, "timetable": {"scheduledArrivalTime": 1611235980000, "actualArrivalTime": 1611236160000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007144_00", "name": "Bahnbrücken", "code": None, "geocoordinates": {"latitude": 49.119447, "longitude": 8.764854}}, "timetable": {"scheduledArrivalTime": 1611236160000, "actualArrivalTime": 1611236340000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
                    {"station": {"evaNr": "8007145_00", "name": "Menzingen (Baden)", "code": None, "geocoordinates": {"latitude": 49.136233, "longitude": 8.775067}}, "timetable": {"scheduledArrivalTime": 1611236280000, "actualArrivalTime": 1611236460000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": None, "info": {"status": 0, "passed": False, "positionStatus": None, "distance": 0, "distanceFromStart": 0}, "delayReasons": None}
                ]
            }
        ],
        "requestedEvaNr": "8000055_00"
    }
```


#### 4. Other APIs
These are other APIs I discovered but didn't investigate in:

3.1. [https://iceportal.de/api1/rs/pois/map/{lat_s}/{lon_s}/{lat_e}/{lon_e}](https://iceportal.de/api1/rs/pois/map/0.000/0.000/1.000/1.000)

3.2. [https://iceportal.de/api1/rs/configs](https://iceportal.de/api1/rs/configs)

3.3. [https://iceportal.de/api1/rs/configs/cities](https://iceportal.de/api1/rs/configs/cities)

#

### Development

> If you would like to develop your own interface you can use sample data from `iceportal_apis.mocking` and derive a class from `iceportal_apis.interfaces.ApiInterface` or `iceportal_apis.interfaces.TestInterface`

```python
from iceportal_apis.mocking.data import load_from_record, SAMPLE_FILE_STATUS

sample_data_status = load_from_record(SAMPLE_FILE_STATUS)
```

> While on a train you can also save api data for later usage
```python
from requests import get

from iceportal_apis.mocking.data import save_record
from iceportal_apis.constants import URL_STATUS

api_call = get(URL_STATUS).json()
save_record("filename.json", api_call)
```

> When not connected to a trains hotspot use test mode

```python
import iceportal_apis as ipa

train = ipa.Train(test_mode=True)
```
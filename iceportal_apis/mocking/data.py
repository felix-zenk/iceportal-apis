from json import loads, dumps
from os.path import join, dirname
from typing import Tuple, Dict, List

STATIC_STATUS = {
    "connection": True,
    "servicelevel": "AVAILABLE_SERVICE",
    "internet": "HIGH",
    "gpsStatus": "VALID",
    "tileY": 303,
    "tileX": 216,
    "series": "011",
    "latitude": 52.766562,
    "longitude": 10.251847,
    "serverTime": 1603913237508,
    "speed": 169,
    "trainType": "ICE",
    "tzn": "Tz1191",
    "wagonClass": "SECOND",
    "connectivity": {
        "currentState": "HIGH",
        "nextState": "WEAK",
        "remainingTimeSeconds": 58
    }
}


STATIC_TRIP = {
    "trip": {
        "tripDate": "2020-10-31",
        "trainType": "ICE",
        "vzn": "881",
        "actualPosition": 159781,
        "distanceFromLastStop": 41632,
        "totalDistance": 708799,
        "stopInfo": {
            "scheduledNext": "8002548_00",
            "actualNext": "8002548_00",
            "actualLast": "8002553_00",
            "actualLastStarted": "8002553",
            "finalStationName": "München Hbf",
            "finalStationEvaNr": "8000261_00"
        },
        "stops": [
            {"station": {"evaNr": "8002553_00", "name": "Hamburg-Altona", "code": None, "geocoordinates": {"latitude": 53.552695, "longitude": 9.935175}}, "timetable": {"scheduledArrivalTime": None, "actualArrivalTime": None, "showActualArrivalTime": None, "arrivalDelay": '', "scheduledDepartureTime": 1604148180000, "actualDepartureTime": 1604148180000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "11", "actual": "11"}, "info": {"status": 0, "passed": True, "positionStatus": "passed", "distance": 0, "distanceFromStart": 0}, "delayReasons": None},
            {"station": {"evaNr": "8002548_00", "name": "Hamburg Dammtor", "code": None, "geocoordinates": { "latitude": 53.560751, "longitude": 9.989566}}, "timetable": { "scheduledArrivalTime": 1604148720000, "actualArrivalTime": 1604148840000, "showActualArrivalTime": True, "arrivalDelay": "+2", "scheduledDepartureTime": 1604148780000, "actualDepartureTime": 1604148900000, "showActualDepartureTime": True, "departureDelay": "+2"}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": True, "positionStatus": "passed", "distance": 3704, "distanceFromStart": 3704}, "delayReasons": None},
            {"station": {"evaNr": "8002549_00", "name": "Hamburg Hbf", "code": None, "geocoordinates": {"latitude": 53.552736, "longitude": 10.006909}}, "timetable": {"scheduledArrivalTime": 1604149080000, "actualArrivalTime": 1604149140000, "showActualArrivalTime": True, "arrivalDelay": "+1", "scheduledDepartureTime": 1604149260000, "actualDepartureTime": 1604149260000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "14", "actual": "14"}, "info": {"status": 0, "passed": True, "positionStatus": "passed", "distance": 1452, "distanceFromStart": 5156}, "delayReasons": None},
            {"station": {"evaNr": "8000147_00", "name": "Hamburg-Harburg", "code": None, "geocoordinates": {"latitude": 53.455908, "longitude": 9.991701}}, "timetable": {"scheduledArrivalTime": 1604149800000, "actualArrivalTime": 1604149980000, "showActualArrivalTime": True, "arrivalDelay": "+3", "scheduledDepartureTime": 1604149920000, "actualDepartureTime": 1604150100000, "showActualDepartureTime": True, "departureDelay": "+3"}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": True, "positionStatus": "passed", "distance": 10817, "distanceFromStart": 15973}, "delayReasons": None},
            {"station": {"evaNr": "8000238_00", "name": "Lüneburg", "code": None, "geocoordinates": {"latitude": 53.249656, "longitude": 10.41989}}, "timetable": {"scheduledArrivalTime": 1604150820000, "actualArrivalTime": 1604151060000, "showActualArrivalTime": True, "arrivalDelay": "+4", "scheduledDepartureTime": 1604150940000, "actualDepartureTime": 1604151240000, "showActualDepartureTime": True, "departureDelay": "+5"}, "track": {"scheduled": "1", "actual": "1"}, "info": {"status": 0, "passed": True, "positionStatus": "passed", "distance": 36529, "distanceFromStart": 52502}, "delayReasons": None},
            {"station": {"evaNr": "8000152_00", "name": "Hannover Hbf", "code": None, "geocoordinates": {"latitude": 52.376761, "longitude": 9.741021}}, "timetable": {"scheduledArrivalTime": 1604154120000, "actualArrivalTime": 1604154120000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604154360000, "actualDepartureTime": 1604154360000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "3", "actual": "3"}, "info": {"status": 0, "passed": True, "positionStatus": "departed", "distance": 107279, "distanceFromStart": 159781}, "delayReasons": [{"code": "38", "text": "Technische Störung an der Strecke"}]},
            {"station": {"evaNr": "8000128_00", "name": "Göttingen", "code": None, "geocoordinates": {"latitude": 51.536815, "longitude": 9.926072}}, "timetable": {"scheduledArrivalTime": 1604156400000, "actualArrivalTime": 1604156400000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604156520000, "actualDepartureTime": 1604156520000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "10", "actual": "10"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 94281, "distanceFromStart": 254062}, "delayReasons": None},
            {"station": {"evaNr": "8003200_00", "name": "Kassel-Wilhelmshöhe", "code": None, "geocoordinates": {"latitude": 51.313114, "longitude": 9.446898}}, "timetable": {"scheduledArrivalTime": 1604157660000, "actualArrivalTime": 1604157660000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604157780000, "actualDepartureTime": 1604157900000, "showActualDepartureTime": True, "departureDelay": "+2"}, "track": {"scheduled": "2", "actual": "2"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 41515, "distanceFromStart": 295577}, "delayReasons": None},
            {"station": {"evaNr": "8000115_00", "name": "Fulda", "code": None, "geocoordinates": {"latitude": 50.554723, "longitude": 9.683977}}, "timetable": {"scheduledArrivalTime": 1604159640000, "actualArrivalTime": 1604159640000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604159760000, "actualDepartureTime": 1604159760000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 85974, "distanceFromStart": 381551}, "delayReasons": None},
            {"station": {"evaNr": "8000260_00", "name": "Würzburg Hbf", "code": None, "geocoordinates": {"latitude": 49.801796, "longitude": 9.93578}}, "timetable": {"scheduledArrivalTime": 1604161740000, "actualArrivalTime": 1604161740000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604161860000, "actualDepartureTime": 1604161860000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "4", "actual": "4"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 85644, "distanceFromStart": 467195}, "delayReasons": None},
            {"station": {"evaNr": "8000284_00", "name": "Nürnberg Hbf", "code": None, "geocoordinates": {"latitude": 49.445616, "longitude": 11.082989}}, "timetable": {"scheduledArrivalTime": 1604165040000, "actualArrivalTime": 1604165040000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604165220000, "actualDepartureTime": 1604165340000, "showActualDepartureTime": True, "departureDelay": "+2"}, "track": {"scheduled": "8", "actual": "8"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 91662, "distanceFromStart": 558857}, "delayReasons": None},
            {"station": {"evaNr": "8000183_00", "name": "Ingolstadt Hbf", "code": None, "geocoordinates": {"latitude": 48.744541, "longitude": 11.437337}}, "timetable": {"scheduledArrivalTime": 1604167080000, "actualArrivalTime": 1604167080000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": 1604167260000, "actualDepartureTime": 1604167260000, "showActualDepartureTime": True, "departureDelay": ''}, "track": {"scheduled": "3", "actual": "3"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 82137, "distanceFromStart": 640994}, "delayReasons": None},
            {"station": {"evaNr": "8000261_00", "name": "München Hbf", "code": None, "geocoordinates": {"latitude": 48.140232, "longitude": 11.558335}}, "timetable": {"scheduledArrivalTime": 1604169720000, "actualArrivalTime": 1604169720000, "showActualArrivalTime": True, "arrivalDelay": '', "scheduledDepartureTime": None, "actualDepartureTime": None, "showActualDepartureTime": None, "departureDelay": ''}, "track": {"scheduled": "18", "actual": "18"}, "info": {"status": 0, "passed": False, "positionStatus": "future", "distance": 67805, "distanceFromStart": 708799}, "delayReasons": None}
        ]
    },
    "connection": None,
    "selectedRoute": {
        "conflictInfo": {
            "status": "NO_CONFLICT",
            "text": None
        },
        "mobility": None
    },
    "active": None
}


STATIC_CONNECTIONS = {
    "8000055_00": {
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
}


DATA_ROOT = join(dirname(__file__), "sample_data")
SAMPLE_FILE_STATUS = join(DATA_ROOT, "status.json")
SAMPLE_FILE_TRIP = join(DATA_ROOT, "trip.json")


def load_from_record(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return loads(file.read())


def save_record(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(dumps(content, indent=4))


class DynamicDataServer:
    def __init__(self):
        self._data_status = load_from_record(SAMPLE_FILE_STATUS)
        self._data_trip = load_from_record(SAMPLE_FILE_TRIP)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.eva_nrs: List[str] = []
        self.stations: Dict[str, Dict] = {}
        self.velocity: int = 0
        self.position: int = 0
        self.geo_position: Tuple[float, float] = (0.0, 0.0)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.init_data()

    def init_data(self):
        pass


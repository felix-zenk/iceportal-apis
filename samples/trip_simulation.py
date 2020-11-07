# Import
import iceportal_apis as ipa
from datetime import timedelta
from time import sleep
from random import random

write_status = {'speed':190, 'trainType': 'ICE'}
write_trip = {'trip': \
            {'tripDate': '', 'trainType': 'ICE', 'vzn': '881', 'stopInfo': { \
                'scheduledNext': '8002553_00', 'actualNext': '8002553_00', 'actualLast': '8002553_00', 'finalStationName': 'München Hbf', 'finalStationEvaNr': '8000261_00'\
                }, \
                'stops': \
                    [\
                        {'station': {'evaNr': '8002553_00', 'name': 'Hamburg-Altona'}, 'timetable': {'actualArrivalTime': None, 'arrivalDelay': '','actualDepartureTime': 1604148180000, 'departureDelay': ''}, 'track': {'actual': '11'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8002548_00', 'name': 'Hamburg Dammtor'}, 'timetable': {'actualArrivalTime': 1604148840000, 'arrivalDelay': '+2', 'actualDepartureTime': 1604148900000, 'departureDelay': '+2'}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8002549_00', 'name': 'Hamburg Hbf'}, 'timetable': {'actualArrivalTime': 1604149140000, 'arrivalDelay': '+1', 'actualDepartureTime': 1604149260000, 'departureDelay': ''}, 'track': {'actual': '14'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000147_00', 'name': 'Hamburg-Harburg'}, 'timetable': {'actualArrivalTime': 1604149980000, 'arrivalDelay': '+3', 'actualDepartureTime': 1604150100000, 'departureDelay': '+3'}, 'track': {'actual': '4'}, 'delayReasons': [{'code':'38', 'text':'Technische Störung an der Strecke'}]}, \
                        {'station': {'evaNr': '8000238_00', 'name': 'Lüneburg'}, 'timetable': {'actualArrivalTime': 1604151060000, 'arrivalDelay': '+4', 'actualDepartureTime': 1604151240000, 'departureDelay': '+5'}, 'track': {'actual': '1'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000152_00', 'name': 'Hannover Hbf'}, 'timetable': {'actualArrivalTime': 1604154120000, 'arrivalDelay': '', 'actualDepartureTime': 1604154360000, 'departureDelay': ''}, 'track': {'actual': '3'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000128_00', 'name': 'Göttingen'}, 'timetable': {'actualArrivalTime': 1604156400000, 'arrivalDelay': '', 'actualDepartureTime': 1604156520000, 'departureDelay': ''}, 'track': {'actual': '10'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8003200_00', 'name': 'Kassel-Wilhelmshöhe'}, 'timetable': {'actualArrivalTime': 1604157660000, 'arrivalDelay': '', 'actualDepartureTime': 1604157900000, 'departureDelay': '+2'}, 'track': {'actual': '2'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000115_00', 'name': 'Fulda'}, 'timetable': {'actualArrivalTime': 1604159640000, 'arrivalDelay': '', 'actualDepartureTime': 1604159760000, 'departureDelay': ''}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000260_00', 'name': 'Würzburg Hbf'}, 'timetable': {'actualArrivalTime': 1604161740000, 'arrivalDelay': '', 'actualDepartureTime': 1604161860000, 'departureDelay': ''}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000284_00', 'name': 'Nürnberg Hbf'}, 'timetable': {'actualArrivalTime': 1604165040000, 'arrivalDelay': '', 'actualDepartureTime': 1604165340000, 'departureDelay': '+2'}, 'track': {'actual': '8'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000183_00', 'name': 'Ingolstadt Hbf'}, 'timetable': {'actualArrivalTime': 1604167080000, 'arrivalDelay': '', 'actualDepartureTime': 1604167260000, 'departureDelay': ''}, 'track': {'actual': '3'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000261_00', 'name': 'München Hbf'}, 'timetable': {'actualArrivalTime': 1604169720000, 'arrivalDelay': '', 'actualDepartureTime': None, 'departureDelay': ''}, 'track': {'actual': '18'}, 'delayReasons': None}\
                    ]\
            }, \
        }


def get_simulated_status():
    return write_status
def get_simulated_trip():
    return write_trip

# Override
ipa.get_status = lambda: get_simulated_status()
ipa.get_trip = lambda: get_simulated_trip()

def clear():
    from os import system, name
    system('cls' if name=='nt' else 'clear')

def getMultiplier():
    try:
        val = float(input('Multiplikator für die Geschwindigkeit: '))
        if val >= 1.0 and val <= 500.0:
            return val
        raise Exception()
    except:
        clear()
        print('Du musst einen korrekten Wert eingeben! (1.0 / 2.0 / 10.0 / 100.0 / ... / 500.0)')
        return getMultiplier()
        
# Variables
time_wait = 1.0/5.0
time_speed = getMultiplier()/(1/time_wait)
eva_numbers = ipa.get_station_eva_numbers()
time_now = ipa.get_departure_time(evaNr=eva_numbers[0])-timedelta(seconds=180)

# Functions
def next_run():
    global write_status, write_trip, time_now
    sleep(time_wait)
    time_now += timedelta(seconds=time_speed)
    try:
        refresh = time_now > ipa.get_departure_time(evaNr=ipa.get_next_station_eva_number())
    except:
        refresh = time_now > ipa.get_departure_time(evaNr=eva_numbers[0])
    try:
        next_station = eva_numbers[eva_numbers.index(ipa.get_next_station_eva_number())+1]
    except:
        next_station = eva_numbers[-1]
    
    if refresh:
        write_trip = {'trip': \
            {'tripDate': '', 'trainType': 'ICE', 'vzn': '881', 'stopInfo': \
                {'scheduledNext': next_station, \
                'actualNext': next_station, \
                'actualLast': ipa.get_next_station_eva_number(), 'finalStationName': 'München Hbf', 'finalStationEvaNr': '8000261_00'\
                }, \
                'stops': \
                    [\
                        {'station': {'evaNr': '8002553_00', 'name': 'Hamburg-Altona'}, 'timetable': {'actualArrivalTime': None, 'arrivalDelay': '','actualDepartureTime': 1604148180000, 'departureDelay': ''}, 'track': {'actual': '11'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8002548_00', 'name': 'Hamburg Dammtor'}, 'timetable': {'actualArrivalTime': 1604148840000, 'arrivalDelay': '+2', 'actualDepartureTime': 1604148900000, 'departureDelay': '+2'}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8002549_00', 'name': 'Hamburg Hbf'}, 'timetable': {'actualArrivalTime': 1604149140000, 'arrivalDelay': '+1', 'actualDepartureTime': 1604149260000, 'departureDelay': ''}, 'track': {'actual': '14'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000147_00', 'name': 'Hamburg-Harburg'}, 'timetable': {'actualArrivalTime': 1604149980000, 'arrivalDelay': '+3', 'actualDepartureTime': 1604150100000, 'departureDelay': '+3'}, 'track': {'actual': '4'}, 'delayReasons': [{'code':'38', 'text':'Technische Störung an der Strecke'}]}, \
                        {'station': {'evaNr': '8000238_00', 'name': 'Lüneburg'}, 'timetable': {'actualArrivalTime': 1604151060000, 'arrivalDelay': '+4', 'actualDepartureTime': 1604151240000, 'departureDelay': '+5'}, 'track': {'actual': '1'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000152_00', 'name': 'Hannover Hbf'}, 'timetable': {'actualArrivalTime': 1604154120000, 'arrivalDelay': '', 'actualDepartureTime': 1604154360000, 'departureDelay': ''}, 'track': {'actual': '3'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000128_00', 'name': 'Göttingen'}, 'timetable': {'actualArrivalTime': 1604156400000, 'arrivalDelay': '', 'actualDepartureTime': 1604156520000, 'departureDelay': ''}, 'track': {'actual': '10'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8003200_00', 'name': 'Kassel-Wilhelmshöhe'}, 'timetable': {'actualArrivalTime': 1604157660000, 'arrivalDelay': '', 'actualDepartureTime': 1604157900000, 'departureDelay': '+2'}, 'track': {'actual': '2'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000115_00', 'name': 'Fulda'}, 'timetable': {'actualArrivalTime': 1604159640000, 'arrivalDelay': '', 'actualDepartureTime': 1604159760000, 'departureDelay': ''}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000260_00', 'name': 'Würzburg Hbf'}, 'timetable': {'actualArrivalTime': 1604161740000, 'arrivalDelay': '', 'actualDepartureTime': 1604161860000, 'departureDelay': ''}, 'track': {'actual': '4'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000284_00', 'name': 'Nürnberg Hbf'}, 'timetable': {'actualArrivalTime': 1604165040000, 'arrivalDelay': '', 'actualDepartureTime': 1604165340000, 'departureDelay': '+2'}, 'track': {'actual': '8'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000183_00', 'name': 'Ingolstadt Hbf'}, 'timetable': {'actualArrivalTime': 1604167080000, 'arrivalDelay': '', 'actualDepartureTime': 1604167260000, 'departureDelay': ''}, 'track': {'actual': '3'}, 'delayReasons': None}, \
                        {'station': {'evaNr': '8000261_00', 'name': 'München Hbf'}, 'timetable': {'actualArrivalTime': 1604169720000, 'arrivalDelay': '', 'actualDepartureTime': None, 'departureDelay': ''}, 'track': {'actual': '18'}, 'delayReasons': None}\
                    ]\
            }, \
        }
    write_status = {'speed':ipa.get_speed()+int(random()*5)-2, 'trainType': 'ICE'}

############################    
# RUN
############################
finished = False
try:
    while not finished:
        status, trip = ipa.get_all()
        clear()
        print(f'Aktuelle Zeit: {time_now.strftime("%d.%m.%Y %H:%M:%S")}')
        print(f'Dies ist: {ipa.get_train_type()} {ipa.get_trip_id()} nach {ipa.get_final_station_name()}')
        print()
        try:
            print(f'Nächste Ankunft: {ipa.get_arrival_time(evaNr=ipa.get_next_station_eva_number()).strftime("%H:%M")}')
        except:
            pass
        print(f'Nächste Station: {ipa.get_next_station_name()}')
        try:
            print(f'Nächste Abfahrt: {ipa.get_departure_time(evaNr=ipa.get_next_station_eva_number()).strftime("%H:%M")}')
        except:
            pass
        
        if ipa.get_delay_status():
            print()
            print(f'Der {ipa.get_train_type()} ist aktuell {ipa.get_delay()} min verspätet')
            if ipa.get_delay_reasons_last_station() != []:
                print(f'Grund: {ipa.get_delay_reasons_last_station()[0]}')
        print()
        print(f'Aktuelle Geschwindigkeit: {ipa.get_speed()}km/h')
        if time_now > (ipa.get_arrival_time(evaNr=eva_numbers[-1]) + timedelta(seconds=180)):
            finished = True
            print('Der Zug ist am Ziel angekommen')
        else:
            try:
                print(f'Restliche Reisedauer: {ipa.convert_time_to_string(ipa.get_arrival_time(evaNr=eva_numbers[-1])-time_now, locale="de")}')
            except ipa.NotInFutureException:
                pass
        next_run()
except KeyboardInterrupt:
    pass
print('\n\nBeende...')
sleep(5)

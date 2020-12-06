#
# REQURIES ICEPORTAL-APIS v1.0.7 or newer
#

# Import
import iceportal_apis as ipa
from datetime import datetime, timedelta
from time import sleep

from sample_data_supplier import get_sample_data_status, get_sample_data_trip, refresh_data
ipa.get_status = lambda: get_sample_data_status()
ipa.get_trip = lambda: get_sample_data_trip()

def clear():
    from os import system, name
    system('cls' if name=='nt' else 'clear')

############################    
# RUN
############################
finished = False
ziel = None
bahnhoefe = ipa.get_station_names()

def chooseMultiplier():
    try:
        mul = float(input('(ENTER für Echtzeit)\nMultiplikator für Zeit: '))
    except:
        mul = 1.0
    if mul < 1.0:
        clear()
        print('Es sind nur Zahlen >= 1.0 erlaubt')
        return chooseMultiplier()
    else:
        return mul

def chooseDestination():
    def choose():
        clear()
        showAll()
        return evaluate(input('Zielbahnhof: '))
    def showAll():
        print('Bitte wähle einen Zielbahnhof aus:\n')
        for station in bahnhoefe:
            print(f' - {station}')
    def evaluate(ziel):
        ziel = ziel.strip()
        while '  ' in ziel:
            ziel = ziel.replace('  ', ' ')
        possible_stations = []
        if ziel != '':
            for station in bahnhoefe:
                if station.startswith(ziel):
                    possible_stations.append(station)
            if len(possible_stations) == 1:
                return possible_stations[0]
            elif len(possible_stations) > 1:
                return chooseFiltered(possible_stations)
            elif len(possible_stations)==0:
                for station in bahnhoefe:
                    if ziel.replace(' ', '') in station or station.lower().startswith(ziel):
                        possible_stations.append(station)
                if len(possible_stations) == 1:
                    return possible_stations[0]
                if len(possible_stations) > 1:
                    return chooseFiltered(possible_stations)
        return choose()
    def chooseFiltered(possible_stations):
        clear()
        print('Deine Eingabe war unklar. Meintest du:')
        for station in possible_stations:
            print(f' - {station}')
        value = input('Zielbahnhof: ')
        for station in possible_stations:
            if value in station:
                return evaluate(value)
            else:
                return chooseFiltered(possible_stations)
    return choose()

#############################
try:
    ziel = chooseDestination()
    print(f'\n - "{ziel}" gewählt\n')
    multiplier = chooseMultiplier()
    refresh_data()
except:
    ziel = None
if ziel in bahnhoefe:
    try:
        simulated_time = datetime.now()
        if multiplier > 60:
            simulated_time = simulated_time.replace(second=0)
        while not finished:
            try:
                status, trip = ipa.get_all()
            except iceportal_apis.NetworkException:
                print('Verbindung verloren.')
                break
            clear()
            print(f'Aktuelle Zeit: {simulated_time.strftime("%d.%m.%Y %H:%M:%S")}')
            print(f'Dies ist: {ipa.get_train_type(status_call=status)} {ipa.get_trip_id(trip_call=trip)} nach {ipa.get_final_station_name(trip_call=trip)}')
            print()
            try:
                if ipa.convert_time_to_string(ipa.get_time_until_next_arrival(trip_call=trip), locale="de", no_seconds=True) != '':
                    print(f'Nächste Ankunft: {ipa.get_arrival_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip)).strftime("%H:%M")} ({ipa.convert_time_to_string(ipa.get_time_until_next_arrival(trip_call=trip), locale="de", no_seconds=True)})')
                else:
                    print(f'Nächste Ankunft: {ipa.get_arrival_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip)).strftime("%H:%M")} (Jetzt)')
            except:
                pass
            print(f'Nächste Station: {ipa.get_next_station_name(trip_call=trip)} (Gleis {ipa.get_next_track(trip_call=trip)})')
            if not ipa.get_next_station_name(trip_call=trip) == ziel:
                try:
                    if ipa.convert_time_to_string(ipa.get_time_until_next_departure(trip_call=trip), locale="de", no_seconds=True) != '':
                        print(f'Nächste Abfahrt: {ipa.get_departure_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip), trip_call=trip).strftime("%H:%M")} ({ipa.convert_time_to_string(ipa.get_time_until_next_departure(trip_call=trip), locale="de", no_seconds=True)})')
                    else:
                        print(f'Nächste Abfahrt: {ipa.get_departure_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip), trip_call=trip).strftime("%H:%M")} (Jetzt)')
                except:
                    pass
            
            if ipa.get_delay_status(trip_call=trip):
                print(f'\nDer {ipa.get_train_type(status_call=status)} ist aktuell {ipa.get_delay(trip_call=trip)} min verspätet')
                if ipa.get_delay_reasons_last_station(trip_call=trip) != []:
                    print(f'Grund: {ipa.get_delay_reasons_last_station(trip_call=trip)[0]}')
            else:
                print(f'\nDer Zug ist pünktlich')
            print(f'\nAktuelle Geschwindigkeit: {ipa.get_speed(status_call=status)}km/h')
            if simulated_time > ipa.get_arrival_time(evaNr=ipa.get_final_station_eva_number(trip_call=trip), trip_call=trip):
                finished = True
                print('Der Zug ist am Ziel angekommen')
            else:
                try:
                    print(f'Ausstieg in {ziel}: {ipa.get_arrival_time(station_name=ziel, trip_call=trip).strftime("%H:%M")} ({ipa.convert_time_to_string(ipa.get_time_until_arrival(station_name=ziel, trip_call=trip), locale="de", no_seconds=True)})')
                    print(f'Noch {int(ipa.get_station_distance(evaNr=ipa.get_next_station_eva_number(trip_call=trip), status_call=status, trip_call=trip))}m bis zum nächsten Bahnhof')
                except ipa.NotInFutureException:
                    pass
            if multiplier <= 60:
                sleep(1/multiplier)
                simulated_time+=timedelta(seconds=1)
            else:
                sleep(60/multiplier)
                simulated_time+=timedelta(minutes=1)
    except KeyboardInterrupt:
        pass
print('\n\nBeende...')
sleep(2)
ipa.autoupdate()

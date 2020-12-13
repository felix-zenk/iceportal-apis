# Import
import iceportal_apis as ipa
from datetime import datetime, timedelta
from time import sleep

def clear():
    from os import system, name
    system('cls' if name=='nt' else 'clear')

def end():
    print('\n\nBeende...')
    sleep(3)
    exit()
############################    
# RUN
############################
try:
    ipa.get_station_names()
except ipa.NotOnTrainException:
    print('Du musst dich in einem Zug befinden um diese Funktion nutzen zu können!')
    end()
ziel = None
finished = False
bahnhoefe = ipa.get_station_names()

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

ziel = chooseDestination()
if ziel in bahnhoefe:
    try:
        while not finished:
            try:
                status, trip = ipa.get_all()
            except iceportal_apis.NetworkException:
                print('Verbindung verloren.')
                break
            clear()
            print(f'Aktuelle Zeit: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')
            print(f'Dies ist: {ipa.get_train_type(status_call=status)} {ipa.get_trip_id(trip_call=trip)} nach {ipa.get_final_station_name(trip_call=trip)}')
            print()
            try:
                if ipa.convert_time_to_string(ipa.get_time_until_next_arrival(trip_call=trip), locale="de") != '':
                    print(f'Nächste Ankunft: {ipa.get_arrival_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip), trip_call=trip).strftime("%H:%M")} ({ipa.convert_time_to_string(ipa.get_time_until_next_arrival(trip_call=trip), locale="de", no_seconds=True)})')
                else:
                    print(f'Nächste Ankunft: {ipa.get_arrival_time(evaNr=ipa.get_next_station_eva_number(trip_call=trip), trip_call=trip).strftime("%H:%M")} (Jetzt)')
            except:
                pass
            print(f'Nächste Station: {ipa.get_next_station_name(trip_call=trip)} (Gleis {ipa.get_next_track(trip_call=trip)})')
            
            print(f'Noch {"{:.1f}".format(int(ipa.get_station_distance(evaNr=ipa.get_next_station_eva_number(trip_call=trip), trip_call=trip))/1000)}km bis zum Bahnhof')
            
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
            if datetime.now() > ipa.get_arrival_time(evaNr=ipa.get_final_station_eva_number(trip_call=trip), trip_call=trip):
                finished = True
                print('Der Zug ist am Ziel angekommen')
            else:
                try:
                    print(f'Ausstieg in {ziel}: {ipa.get_arrival_time(station_name=ziel, trip_call=trip).strftime("%H:%M")} ({ipa.convert_time_to_string(ipa.get_time_until_arrival(station_name=ziel, trip_call=trip), locale="de", no_seconds=True)})')
                except ipa.NotInFutureException:
                    pass
                    
            sleep(0.5)
    except KeyboardInterrupt:
        pass
end()

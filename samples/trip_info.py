# Import
import iceportal_apis as ipa
from datetime import datetime, timedelta
from time import sleep


def clear():
    from os import system, name
    system('cls' if name == 'nt' else 'clear')


def main():
    def choose():
        clear()
        print("Choose a station:")
        stations = train.get_all_stations()
        for i in range(len(stations)):
            print(f"{i+1}. {stations[i].name}")
        selection = input("> ")
        try:
            return stations[int(selection.strip())-1]
        except ValueError:
            for station in stations:
                if station.name.lower().startswith(selection.lower()):
                    return station
        return choose()

    train = ipa.Train(test_mode=False)
    end_station = choose()
    print(f'\n - Chose {end_station}!\n')

    finished = False
    while not finished:
        train.refresh()  # Get the newest values
        clear()
        print("\nThis is:", train.get_train_type().name, train.get_trip_id(), "to", train.get_final_station().name)
        next_station = train.get_next_station()
        print("Next station:", next_station.name, f"(Platform {train.get_platform(next_station)})")
        print(int(train.get_time_until_arrival(next_station).total_seconds()/60), "minutes until next arrival",
              f"({train.get_arrival_time(next_station).strftime('%H:%M')})")
        if train.is_delayed():
            print("This train is delayed by", int(train.get_current_delay().total_seconds()/60), "minutes")
        print("Internet connection status is:", train.get_internet_status().name.lower().capitalize(),
              f"({train.get_next_internet_status().name.lower().capitalize()} in "
              f"{int(train.get_time_until_internet_change().total_seconds())} seconds)")
        sleep(1)  # Wait some time


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

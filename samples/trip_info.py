# Import
from onboardapis.trains import Station
from onboardapis.trains.germany.db import ICEPortal

# import iceportal_apis as ipa
from datetime import datetime
from time import sleep


def clear():
    from os import system, name
    system('cls' if name == 'nt' else 'clear')


class InformationDisplayTrain(ICEPortal):
    def choose_station(self, message: str) -> Station:
        clear()
        print(message)
        for idx, station in enumerate(self.stations.values(), start=1):
            print(f"{idx: >2}: {station.name}")
        selection = input("> ")
        try:
            return list(self.stations.values())[int(selection.strip()) - 1]  # try to get station by idx
        except ValueError:
            for station in self.stations.values():
                if station.name.lower().startswith(selection.lower()):
                    return station  # get station by name
        return self.choose_station(message)

    def print_trip(self, start: Station, end: Station):
        clear()
        # Train information
        if self.name is None:
            print("\nThis is:", self.type, self.number, "to", self.destination.name)
        else:
            print("\nThis is:", self.type, f"'{self.name}'", "to", self.destination.name)
        print("Next station:", self.current_station.name, f"(Platform {self.current_station.platform.actual})")
        print((self.current_station.arrival.actual - datetime.now()).total_seconds() / 60, "minutes until next arrival",
              f"({self.current_station.arrival.actual.strftime('%H:%M')})")
        if self.delay:
            print("This train is delayed by", int(self.delay / 60), "minutes")

        # my trip
        trip_distance = end.distance - start.distance
        travelled_distance = self.distance - start.distance
        fraction = travelled_distance / trip_distance
        print(f"My trip: {start.name} {'=' * int(fraction * 5)}>{' ' * (20 - int(fraction*5))} {end.name}")
        print(f"Distance travelled {travelled_distance/1000:.1f} km / {trip_distance/1000:.1f} km "
              f"({fraction * 100:.2f} %)")

        # Internet status
        internet_now, internet_next, internet_change_in = self.internet_connection()
        print("Internet connection status is:", internet_now.lower().capitalize(),
              f"({internet_next.lower().capitalize()} in "
              f"{internet_change_in} seconds)")
        sleep(3)  # Wait some time

    def main_loop(self):
        start = self.choose_station("Choose a start")
        end = self.choose_station("Choose an end station")
        while self.connected:
            self.print_trip(start, end)


if __name__ == '__main__':
    try:
        with InformationDisplayTrain() as information_train:
            information_train.main_loop()
    except KeyboardInterrupt:
        exit()

import datetime
# import iceportal_apis as ipa

from time import sleep

from onboardapis.trains.germany.db import ICEPortal
from onboardapis.utils.conversions import ms_to_kmh


class InformationDisplayTrain(ICEPortal):
    def print_next_station(self):
        """
        # Information related to the next station
        Function for getting the next train station and information on the current status (delay, track, ...)
        """
        print(f"Next stop: '{self.current_station.name}' at {self.current_station.arrival.actual.strftime('%H:%M')}"
              f" on platform {self.current_station.platform.actual}.")
        print(f'Arrival in {self.current_station.arrival.actual - datetime.datetime.now()}')
        if self.delay:
            print(f'This train is {self.delay/60:.1f} min delayed')
            if self.delay_reasons() is not None:
                print(f"Reasons: '{'. '.join(self.delay_reasons())}'")
        print(f"Stations on this trip: {', '.join(station.name for station in self.stations.values())}")

    def print_speed(self):
        """
        # Information related to the trains speed
        Function for getting the train type and the current speed of the train.
        """
        print(f'This {self.type} {self.number}{f" {self.name}" if self.name is not None else ""} '
              f'is currently going {ms_to_kmh(self.speed)} km/h')

    
def main():
    with InformationDisplayTrain() as information_train:
        while information_train.connected:
            information_train.print_next_station()
            information_train.print_speed()
            sleep(3)


# Entry
if __name__ == "__main__":
    main()

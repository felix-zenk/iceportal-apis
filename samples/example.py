# Import iceportal_apis
import iceportal_api as ipas

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

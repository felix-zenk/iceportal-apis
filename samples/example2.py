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
            print(f'Reason: "{ipa.get_delay_reasons_last_station(trip_call=call)}"')
    
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
# Import iceportal_apis
import iceportal_apis as ipa


def example_next_station():
    """
    # Information related to the next station
    Function for getting the next train station and information on the current status (delay, track, ...)
    """
    print(f'Next stop: "{train.get_next_station()}" at {train.get_next_arrival_time()}'
          f' on platform {train.get_next_track()}.')
    print(f'Arrival in {train.get_time_until_next_arrival()}')
    if train.is_delayed():
        print(f'This train is {train.get_current_delay()} min delayed')
        if train.get_current_delay_reasons():
            print(f'Reason: "{train.get_current_delay_reasons()}"')
    print(train.get_all_stations())


def example_speed():
    """
    # Information related to the trains speed
    Function for getting the train type and the current speed of the train.
    """
    print(f'This {train.get_train_type().name} is currently going {train.get_speed()}km/h')

    
# Entry
if __name__ == "__main__":
    train = ipa.Train(test_mode=False)
    example_next_station()
    example_speed()
    input()  # keep the window opened

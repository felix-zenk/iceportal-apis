from enum import unique, Enum


@unique
class InterfaceStatus(Enum):
    UNKNOWN = None
    ERROR = -1
    IDLE = 0
    FETCHING = 1


@unique
class WagonClass(Enum):
    UNKNOWN = None
    FIRST = 1
    SECOND = 2


@unique
class TrainType(Enum):
    UNKNOWN = None
    IC = "IC"
    ICE = "ICE"


@unique
class Internet(Enum):
    UNKNOWN = None  # Client can't tell
    NO_INFO = -1  # Train can't tell
    NO_INTERNET = 0
    UNSTABLE = 1
    WEAK = 2
    MIDDLE = 3
    HIGH = 4


# ~~iceportal_apis~~

---

No longer actively developed in favor of the [onboardAPIs](https://github.com/felix-zenk/onboardapis) ([PyPI](https://pypi.org/project/onboardapis)) project which includes APIs for different providers.
---

---

[![PyPI version](https://badge.fury.io/py/iceportal_apis.svg)](https://pypi.org/project/iceportal-apis)
[![PyPI-Versions](https://img.shields.io/pypi/pyversions/iceportal-apis)](https://pypi.org/project/iceportal-apis)
[![GitHub](https://img.shields.io/badge/license-MIT-green)](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE)

### Description
This module interacts with the onboard APIs of the Deutsche Bahn ICE trains.\
It can do various things from reading the trains' velocity to telling you the distance to and the delay at the next station.\
This is an unofficial project and not supported by [`Deutsche Bahn AG`](https://www.deutschebahn.com/de/konzern).

> Note, that this module will only work correctly while you are on a train and connected to its WiFi-Hotspot.

### Installation
* Available on PyPI
    ```shell
    $ python -m pip install iceportal_apis
    ```

### Usage

```python
import iceportal_apis as ipa

train = ipa.Train()

while True:
    # Request new data from the api
    # train.refresh()  # obsolete, because onboardapis handles refreshing
    
    # Process data  (uses onboardapis under the hood)
    print(train.get_train_type().name)
    next_station = train.get_next_station()

    . . .
```

### License
> **This software is distributed under the MIT License, please see [`LICENSE`](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE) for detailed information.**

### API documentation

#### 1. Status API
The Status API is available at [https://iceportal.de/api1/rs/status](https://iceportal.de/api1/rs/status)

#### 2. Trip API
The Trip API is available at [https://iceportal.de/api1/rs/tripInfo/trip](https://iceportal.de/api1/rs/tripInfo/trip)

#### 3. Connections API
The Connecting trains API can be found at [https://iceportal.de/api1/rs/tripInfo/connection/{eva_number}](https://iceportal.de/api1/rs/tripInfo/connection/8000000_00)

#### 4. Other APIs
These are other APIs I discovered but didn't investigate in:

4.1. [https://iceportal.de/api1/rs/pois/map/{lat_s}/{lon_s}/{lat_e}/{lon_e}](https://iceportal.de/api1/rs/pois/map/0.000/0.000/1.000/1.000)

4.2. [https://iceportal.de/api1/rs/configs](https://iceportal.de/api1/rs/configs)

4.3. [https://iceportal.de/api1/rs/configs/cities](https://iceportal.de/api1/rs/configs/cities)

4.4. [https://iceportal.de/bap/api/availabilities](https://iceportal.de/bap/api/availabilities)

4.5. [https://iceportal.de/bap/api/bap-service-status](https://iceportal.de/bap/api/bap-service-status)

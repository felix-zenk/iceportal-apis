# iceportal_apis

[![PyPI version](https://img.shields.io/badge/pypi-v1.1.0-yellow)](https://pypi.org/project/iceportal-apis)
[![Supported Python versions](https://img.shields.io/badge/Python-3-blue)](https://pypi.org/project/iceportal-apis)
[![GitHub](https://img.shields.io/badge/license-MIT-green)](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE)

### Description
This module interacts with the onboard APIs of the Deutsche Bahn ICE trains.\
It can do various things from reading the trains' velocity to telling you the distance to and the delay at the next station.\
( Explore all functions below at [`Documentation`](https://github.com/felix-zenk/iceportal-apis#documentation) )\
This is an unofficial project and not supported by [`Deutsche Bahn AG`](https://www.deutschebahn.com/de/konzern).
> Note, that this module will only work correctly while you are on a train and connected to its WiFi-Hotspot.\
> However a basic simulation for offline research is also included in this module

#

### Installation
* Available on PyPI
    ```shell
    $ python -m pip install iceportal_apis
    ```
  for the newest (unstable) version install the module from GitHub
    ```shell
    $ python -m pip install git+https://github.com/felix-zenk/iceportal-apis.git
    ```

> Or download the source files from: [PyPI (web)](https://pypi.org/project/iceportal-apis/#files), 
[GitHub](https://github.com/felix-zenk/iceportal-apis)
> and install via setup.py
>
> The latest version is: v1.1.1 (13.10.2021)

#

### Usage
> Example code is available in the file [`example.py`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples/example.py) and other files in [`samples`](https://github.com/felix-zenk/iceportal-apis/blob/main/samples).
>
> The basic usage consists of requesting new data from the api, then processing it with the modules functions.

```python
import iceportal_apis as ipa

train = ipa.Train()

while True:
    # Request new data from the api
    train.refresh()
    
    # Process data
    print(train.get_train_type().name)
    next_station = train.get_next_station()

    . . .
```

> For GUI applications you can also specify automatic api polling

```python
train = ipa.Train(auto_refresh=True)
```

#

### License
> **This software is distributed under the MIT License, please see [`LICENSE`](https://github.com/felix-zenk/iceportal-apis/blob/main/LICENSE) for detailed information.**

#

### <div id="documentation">Documentation</div>

1. **Work**
    1. in\
        1\. progress



#

### <div id="api">API documentation</div>

#### 1. Status API
The Status API is available at [https://iceportal.de/api1/rs/status](https://iceportal.de/api1/rs/status)

A sample response can be found at:
```python
iceportal_api.mocking.data.STATIC_STATUS
```

#### 2. Trip API
The Trip API is available at [https://iceportal.de/api1/rs/tripInfo/trip](https://iceportal.de/api1/rs/tripInfo/trip)

A sample response can be found at:
```python
iceportal_api.mocking.data.STATIC_TRIP
```

#### 3. Connections API
The Connecting trains API can be found at [https://iceportal.de/api1/rs/tripInfo/connection/{eva_number}](https://iceportal.de/api1/rs/tripInfo/connection/8000000_00)

A sample response can be found at:
```python
iceportal_api.mocking.data.STATIC_CONNECTIONS
```


#### 4. Other APIs
These are other APIs I discovered but didn't investigate in:

4.1. [https://iceportal.de/api1/rs/pois/map/{lat_s}/{lon_s}/{lat_e}/{lon_e}](https://iceportal.de/api1/rs/pois/map/0.000/0.000/1.000/1.000)

4.2. [https://iceportal.de/api1/rs/configs](https://iceportal.de/api1/rs/configs)

4.3. [https://iceportal.de/api1/rs/configs/cities](https://iceportal.de/api1/rs/configs/cities)

#

### Development

> If you would like to develop your own interface you can use sample data from `iceportal_apis.mocking` and derive a class from `iceportal_apis.interfaces.ApiInterface` or `iceportal_apis.interfaces.TestInterface`

```python
from iceportal_apis.mocking.data import load_from_record, SAMPLE_FILE_STATUS

sample_data_status = load_from_record(SAMPLE_FILE_STATUS)
```

> While on a train you can also save api data for later usage
```python
from requests import get

from iceportal_apis.mocking.data import save_record
from iceportal_apis.constants import URL_STATUS

api_call = get(URL_STATUS).json()
save_record("filename.json", api_call)
```

> When not connected to a trains hotspot use test mode

```python
import iceportal_apis as ipa

train = ipa.Train(test_mode=True)
```

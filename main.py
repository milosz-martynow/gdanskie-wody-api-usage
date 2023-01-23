"""Application that pull the data https://pomiary.gdanskiewody.pl/rest/stations
and prints it in console
"""

import datetime
from time import sleep
from typing import List, Tuple

import requests

API_KEY: str = "e5ac1ec44f3d4b86a10273000d526ccf"
URL_BASE: str = "https://pomiary.gdanskiewody.pl/rest/measurements"
STATION_NUMBER: str = "3"
MEASUREMENTS: List[str] = [
    "rain",
    "water",
    "flow",
    "winddir",
    "windlevel",
    "temp",
    "pressure",
    "humidity",
    "sun",
]
DURATION: int = 1


def create_urls(
    url_base: str, station_number: str, measurements: List[str], measurement_time: str
) -> List[str]:
    """Create single datetime URL to pull measurement data."""
    return [
        f"{url_base}/{station_number}/{measurement}/{measurement_time}"
        for measurement in measurements
    ]


def get_meteorological_data(api_key: str, url: str) -> dict:
    """Pull data from specific URL, for a personal API key."""
    try:
        measurements = requests.get(
            url, headers={"Authorization": "Bearer {}".format(api_key)}
        ).json()
        measurements["data"] = {data[0]: data[1] for data in measurements["data"]}
    except:
        measurements = {}

    return measurements


def run(
    api_key: str = API_KEY,
    url_base: str = URL_BASE,
    station_number: str = STATION_NUMBER,
    measurements: str = MEASUREMENTS,
) -> Tuple[str, str, dict]:
    """Function that creates URL (or URL's), download,
    aggregate and print meteorological data.
    """

    actual_time = datetime.datetime.now()
    actual_date = actual_time.strftime("%Y-%m-%d")
    actual_date_with_hour = actual_time.strftime("%Y-%m-%d %H:00:00")

    urls = create_urls(
        url_base=url_base,
        station_number=station_number,
        measurements=measurements,
        measurement_time=actual_date,
    )

    data = {
        measurement: get_meteorological_data(api_key=api_key, url=url)
        for measurement, url in zip(measurements, urls)
    }

    actual_data = {}
    for key, val in data.items():
        try:
            actual_data[key] = val[actual_date_with_hour]
        except KeyError:
            actual_data[key] = None

    return actual_time.strftime("%Y-%m-%d %H:%M:%S"), actual_date_with_hour, actual_data


if __name__ == "__main__":
    while True:
        print(run())
        sleep(DURATION)

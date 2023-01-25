"""Application that pull the data https://pomiary.gdanskiewody.pl/rest/stations
and prints it in console
"""

import datetime
from time import sleep
from typing import List, Optional, Tuple

import requests

API_KEY: Optional[str] = None
URL_BASE: str = "https://pomiary.gdanskiewody.pl/rest/measurements"
STATION_NUMBER: str = "13"
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


def create_url(
    url_base: str, station_number: str, measurement: str, measurement_time: str
) -> str:
    """Create single URL to the meteorological data"""
    return f"{url_base}/{station_number}/{measurement}/{measurement_time}"


def create_urls(
    url_base: str, station_number: str, measurements: List[str], measurement_time: str
) -> List[str]:
    """Create list of URLs to the meteorological data at one measurement_time."""
    return [
        create_url(
            url_base=url_base,
            station_number=station_number,
            measurement=measurement,
            measurement_time=measurement_time,
        )
        for measurement in measurements
    ]


def get_meteorological_data(api_key: str, url: str) -> dict:
    """Pull data from specific URL, for a personal API key."""

    if api_key is None:
        raise TypeError("No API key given.")

    try:
        return requests.get(
            url, headers={"Authorization": "Bearer {}".format(api_key)}
        ).json()

    # pylint: disable=bare-except
    except:
        return {}


def manipulate_meteorological_data(measurements: dict, date_with_hour: str) -> dict:
    """Preprocess meteorological data dictionary.
    1. Replace whole day list of lists wit date time and value into
    dictionary where key is datetime and value is measurement value.
    2. Extract only one key of date_with_hour.
    """

    extracted_measurements = {}
    for measurement_key, measurement_data in measurements.items():
        actual_data = measurements[measurement_key].get("data", [])
        extracted_measurements[measurement_key] = {d[0]: d[1] for d in actual_data}.get(
            date_with_hour, None
        )

    return extracted_measurements


def run(
    api_key: str = API_KEY,
    url_base: str = URL_BASE,
    station_number: str = STATION_NUMBER,
    measurements: str = MEASUREMENTS,
) -> Tuple[str, str, dict]:
    """Function that creates URL (or URLs), download,
    aggregate and print meteorological data.

    NOTE: data_time must be one hour delayed, due to data acquisition delay.
    """

    data_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    data_date = data_time.strftime("%Y-%m-%d")
    data_date_with_hour = data_time.strftime("%Y-%m-%d %H:00:00")

    urls = create_urls(
        url_base=url_base,
        station_number=station_number,
        measurements=measurements,
        measurement_time=data_date,
    )

    data = {
        measurement: get_meteorological_data(api_key=api_key, url=url)
        for measurement, url in zip(measurements, urls)
    }

    data = manipulate_meteorological_data(
        measurements=data, date_with_hour=data_date_with_hour
    )

    return data_date_with_hour, data


if __name__ == "__main__":
    while True:
        print(run())
        sleep(DURATION)

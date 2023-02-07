import pytest
import requests

from weatcher import AccuWeather
from unittest.mock import patch


class ResponseGetMock(object):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def raise_for_status():
        pass

    def json():
        return [
            {
                "Version": 1,
                "Key": "2696858",
                "Type": "City",
                "Rank": 85,
                "LocalizedName": "Warszawa",
            }
        ]


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture(params=["Warszawa", "Gdansk"], name="weatcher")
def fixture_weatcher(request, monkeypatch):
    my_weatcher = AccuWeather()

    def monkey_return(url, params):
        return ResponseGetMock

    monkeypatch.setattr(requests, "get", monkey_return)

    my_weatcher.city_token = request.param
    yield my_weatcher


def test_weatcher_initialization():
    assert AccuWeather


def test_weatcher_set_city(monkeypatch):
    weatcher = AccuWeather()

    def monkey_get_city(city: str):
        if city == "Gdansk":
            return "275174"
        return None

    monkeypatch.setattr(weatcher, "get_city", monkey_get_city)

    weatcher.city_token = "Gdansk"
    assert (weatcher.city_token, "275174")


WEATCHER_API = {
    "DailyForecasts": [
        {
            "Date": "2023-01-27T07:00:00+01:00",
            "EpochDate": 1674799200,
            "Temperature": {
                "Minimum": {"Value": -2.6, "Unit": "C", "UnitType": 17},
                "Maximum": {"Value": 3.5, "Unit": "C", "UnitType": 17},
            },
        }
    ]
}


# Unit test patching
@patch.object(AccuWeather, "get_forecasts", return_value=WEATCHER_API)
def test_weatcher_get_forecasts(weatcher_mock, weatcher):
    with patch(
        "weatcher.AccuWeather.get_forecasts", return_value=WEATCHER_API
    ):
        assert (weatcher.get_forecasts(), dict)


# Using monkeypatch with pytests patching
def test_weatcher_get_day_temperature(weatcher, monkeypatch):
    def get_forecasts():
        return WEATCHER_API

    monkeypatch.setattr(weatcher, "get_forecasts", get_forecasts)
    weatcher.store_forecasts()
    assert (
        weatcher.get_day_temperature(),
        "Date: 27.01.2023, temperature: 0.4°C",
    )

#!/usr/bin/env python3
import argparse
import os
import logging
import requests

from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')
ACCUWEATHER_MIRROR_URL = os.getenv('ACCUWEATHER_MIRROR_URL')


class AccuWeather:
    """
    The class for interacting with API AccuWeather.
    :param city:
    :type city: str
    :param __api_key:
    :type __api_key: str
    :param accuweather_url:
    :type accuweather_url: str
    """

    __name__ = "forecast"
    __author__ = "Kamil Mirończuk"
    __license__ = "GNU General Public License v3.0"
    __version__ = "1.1"
    __status__ = "production"

    def __init__(self, city: str, api_key: str = API_KEY, accuweather_url: str = ACCUWEATHER_MIRROR_URL):
        self.__api_key = api_key
        self.accuweather_url = accuweather_url
        self.city_id = self.__get_city_id(city)
        self.forecasts = self.__get_forecasts()

    def __str__(self):
        return "Custom API for AccuWeather"

    def __get_average_temperature(self) -> float:
        """
        returns the average temperature based on the currently setting city
        :returns: returns the average temperature
        :rtype: float
        """
        try:
            temperature = self.forecasts['DailyForecasts'][0]['Temperature']
            max_temperature: float = temperature['Minimum']['Value']
            min_temperature: float = temperature['Maximum']['Value']
            average_temperature: float = (min_temperature + max_temperature) / 2
        except:
            logging.error("Date cannot be set. Get the weather forecast first.")
            raise SystemExit()

        return average_temperature

    def __get_date_from_response(self) -> str:
        """
        returns the date based on received weather forecast
        :returns: returns date
        :rtype: str
        """
        if self.forecasts:
            forecasts_date_iso: str = self.forecasts['DailyForecasts'][0]['Date']
            forecasts_date = datetime.fromisoformat(forecasts_date_iso).strftime("%d.%m.%Y")
        else:
            logging.warning('Get the weather forecast first.')
            raise SystemExit()

        return forecasts_date

    def __get_forecasts(self) -> dict:
        """
        retrieves weather for a previously set city
        :returns: returns forecasts
        :rtype: dict
        """
        try:
            r = requests.get(
                f"{self.accuweather_url}/forecasts/v1/daily/1day/{self.city_id}",
                params={
                    "apikey": self.__api_key,
                    "metric": "true"
                })
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error: {}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting: {}".format(errc))
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error: {}".format(errt))
        except requests.exceptions.RequestException as err:
            logging.error("Request Error: {}".format(err))

        try:
            response: dict = r.json()
        except:
            logging.error("An error occurred while adjusting forecasts parameters")
            raise SystemExit()

        return response

    def get_day_temperature(self):
        """prints the temperature of the day on the screen"""
        actual_date: str = self.__get_date_from_response()
        average_temperature: float = self.__get_average_temperature()

        return f"Date: {actual_date}, temperature: {average_temperature:.1f}°C"

    def __get_city_id(self, city: str) -> str:
        """
        get the current city based on the name taken from the api
        :param city:
        :type city: str
        :returns: returns city id
        :rtype: str
        """
        try:
            r = requests.get(
                f"{self.accuweather_url}/locations/v1/cities/search?q={city}",
                params={
                    "apikey": self.__api_key,
                    "metric": "true"
                })
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error: {}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting: {}".format(errc))
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error: {}".format(errt))
        except requests.exceptions.RequestException as err:
            logging.error("Request Error: {}".format(err))

        try:
            response: dict = r.json()
            cityId: str = response[0].get('Key')
        except:
            logging.error("An error occurred while adjusting city parameter")
            raise SystemExit()

        return cityId


def parse_args():
    parser = argparse.ArgumentParser(prog='forecasts')
    parser.add_argument('city', help='City name')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    args = parser.parse_args()

    try:
        loglevel = {
            0: logging.ERROR,
            1: logging.WARN,
            2: logging.INFO}[args.verbose]
    except KeyError:
        loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(message)s',
                        filename='logs.log',)
    console = logging.StreamHandler()
    logging.getLogger().setLevel(loglevel)
    logging.getLogger('').addHandler(console)
    return args


def main(args, env):
    if args.city:
        logging.info('Program started')
        instance = AccuWeather(args.city)
        print(instance.get_day_temperature())


if __name__ == '__main__':
    main(parse_args(), os.environ)

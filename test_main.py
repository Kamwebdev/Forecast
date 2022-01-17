import unittest

from datetime import datetime
from main import AccuWeather
import requests


class TestAccuWeather(unittest.TestCase):

    def test_get_city_id(self):
        c = AccuWeather('gdansk')
        result = c.city_id
        self.assertEqual(result, "1-275174_1_AL")

    def test_get_temperature(self):
        c = AccuWeather('gdansk')
        result = c.forecasts['DailyForecasts'][0]['Temperature']
        self.assertIn("Minimum", result)

    def test_temperature_unit(self):
        c = AccuWeather('gdansk')
        result = c.forecasts['DailyForecasts'][0]['Temperature']
        self.assertIn('C', result['Maximum']['Unit'])
        self.assertIn('C', result['Maximum']['Unit'])

    def test_get_date_forecasts(self):
        c = AccuWeather('gdansk')
        result = c._AccuWeather__get_date_from_response()
        self.assertEqual(result, datetime.now().strftime("%d.%m.%Y"))

    def test_program_output(self):
        c = AccuWeather('gdansk')
        result = c.get_day_temperature()
        self.assertRegex(result, "Date: [\d]{1,2}.[\d]{1,2}.[\d]{4}, temperature: [\d]{1}.[\d]{1}°C")

    def test_apikey(self):
        c = AccuWeather('gdansk')
        response = requests.get(
            f"{c.accuweather_url}/forecasts/v1/daily/1day/1-275174_1_AL",
            params={
                "apikey": c._AccuWeather__api_key,
                "metric": "true"
            })
        self.assertEqual(response.status_code, 200)

    '''
    def test_get_city_id_raise(self):

        with self.assertRaises(Exception) as context:
            c = AccuWeather('gdansk')
            c.__get_city_id('1-275174_1_AL')

        the_exception = context.exception
        self.assertEqual(the_exception.error_code, 3)
    '''


if __name__ == '__main__':
    unittest.main()

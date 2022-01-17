
# Forecast

Modern python3 app for interacting with API AccuWeather.

## Installation:
1.  Create file .env :
```
API_KEY = '<your api key>'  
ACCUWEATHER_MIRROR_URL = 'http://dataservice.accuweather.com'
```
2.  Execute:
```
python3 -m venv myvenv
[linux] source myvenv/bin/activate
[windows] myvenv\Scripts\activate.bat
pip3 install -r requirements.txt
```
## Running the sample
```
python.exe main.py gdansk -v
```
Output:
```
Date: 16.01.2022, temperature: 1.6°C
```
## Running the tests
```
python -m unittest test_main.py
```

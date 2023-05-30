from docopt import docopt
from requests import get

doc = """ 
A simple utlity to get weather details of a city.
Usage:
    whats_the_weather.py --api <API_KEY> --city <CITY> [--wind]
    whats_the_weather.py (-h | --help)
    
Options:
    -h --help   HELP.
    -a --api <API_KEY>  API KEY.
    -c --city <CITY>   CITY NAME.
    -w --wind  Optional SHOW WIND DETAILS.
"""


class FailedToFetchWeatherData(Exception):
    """ Exception raised when failed to fetch weather data"""


class Weather:
    """
    This class is used to get weather details of a city.
    """

    def __init__(self):
        self.location = None
        self.api_key = None
        self.weather_data = None
        self.weather_forecast = {}

    def _get_weather(self):
        """
        This method is used to get weather details of a city.
        """
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + self.api_key + "&q=" + self.location
        response = get(complete_url)
        x = response.json()
        if x["cod"] == 200:
            self.weather_data = x
        elif x["cod"] == 401:
            raise FailedToFetchWeatherData("Error : Invalid API key")
        else:
            raise FailedToFetchWeatherData(f"Error : The given city {self.location} is not found")

        # Fetch the main weather details
        self._get_main()

    def _get_main(self):
        """ Returns the weather details under main tag"""
        _w = self.weather_data["main"]
        self.weather_forecast = {
            "Temperature (in kelvin unit)": _w["temp"],
            "Pressure (in hPa unit)": _w["pressure"],
            "Humidity (in percentage)": _w["humidity"],
            "Description": self.weather_data["weather"][0]["description"]
        }

    def _get_wind(self):
        """ Returns the wind forecast details"""
        _w = self.weather_data["wind"]
        self.weather_forecast["Wind Speed "] = _w["speed"],
        self.weather_forecast["Wind Direction "] = _w["deg"]

    def get_weather(self, api_key, city, wind):
        """
        This method is used to get weather details of a city.
        """
        self.api_key = api_key
        self.location = city
        self._get_weather()
        if wind:
            self._get_wind()

        print(''.join(['{0} \t{1}\n'.format(k, v) for k, v in self.weather_forecast.items()]))


if __name__ == "__main__":
    args = docopt(doc)
    api = args.get("--api")
    city = args.get("--city")
    wind = args.get("--wind")
    weather_report = Weather()
    weather_report.get_weather(api, city, wind)

"""
Support for the Meteoinfo.by service.

"""
import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from homeassistant.components.weather import (
    WeatherEntity)
from homeassistant.const import (
    TEMP_CELSIUS, CONF_NAME)
from custom_components.meteoinfo import CONF_CITY_CODE
from homeassistant.util import Throttle

DEFAULT_NAME = 'Meteoinfo.by'
ATTRIBUTION = 'Data provided by Pogoda.by'

MIN_TIME_BETWEEN_FORECAST_UPDATES = timedelta(minutes=30)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

PLATFORM_SCHEMA = vol.Schema({
}, extra=vol.ALLOW_EXTRA)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CITY_CODE, default='26850'): cv.string,
    vol.Optional(CONF_NAME, default='Meteoradar'): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the OpenWeatherMap weather platform."""

    name = config.get(CONF_NAME)
    city = config.get(CONF_CITY_CODE)
    data = WeatherData(city)

    add_devices([MeteoInfoWeather(
        name, data)], True)


class MeteoInfoWeather(WeatherEntity):
    """Implementation of an OpenWeatherMap sensor."""

    def __init__(self, name, data):
        """Initialize the sensor."""
        self._name = name
        self._data = data
        self.forecast_data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def condition(self):
        """Return the current condition."""
        return self._data.data.conditions

    @property
    def temperature(self):
        """Return the temperature."""
        return float(self._data.data.temperature)

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def pressure(self):
        """Return the pressure."""
        return float(self._data.data.pressure)

    @property
    def humidity(self):
        """Return the humidity."""
        return float(self._data.data.humidity)

    @property
    def wind_speed(self):
        """Return the wind speed."""
        return float(self._data.data.wind[:2])

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    def update(self):
        """Get the latest data from OWM and updates the states."""
        self._data.update()


class WeatherData:
    """Get the latest data from meteoinfo."""

    def __init__(self, city_code):
        """Initialize the data object."""
        self.city_code = city_code
        self.data = None
        self.forecast_data = None
        self.update()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from site."""
        import urllib

        url = 'http://pogoda.by/?city=' + str(self.city_code)

        from pyquery import PyQuery

        conn = urllib.request.urlopen(url)
        data = conn.read()
        conn.close()
        page = PyQuery(data)
        text = page.find("div#cover table tr:first td:first p").text()
        self.data = WeatherConditionsData(text)

    # @Throttle(MIN_TIME_BETWEEN_FORECAST_UPDATES)
    def update_forecast(self):
        """Get the latest forecast from site."""


class WeatherConditionsData:
    def __init__(self, string_data):
        """Initialize the sensor."""
        data_splitlines = string_data.splitlines()
        # self.temp_value = data_splitlines[1][len("Температура воздуха") + 1:-2]
        # self._temperature = self.temp_value[1:] if self.temp_value.rindex('+') != -1 else self.temp_value
        self._temperature = data_splitlines[1][len("Температура воздуха") + 1:-2]
        self._wind = data_splitlines[2][len("Ветер") + 1:]
        self._conditions = data_splitlines[3]
        self._humidity = data_splitlines[4][len("Влажность") + 1:-1]
        self._pressure = data_splitlines[6][1:-4]

    @property
    def conditions(self):
        return self._conditions

    @property
    def temperature(self):
        return self._temperature

    @property
    def wind(self):
        return self._wind

    @property
    def humidity(self):
        return self._humidity

    @property
    def pressure(self):
        return self._pressure

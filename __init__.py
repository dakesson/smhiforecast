import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import requests
import csv 
import logging
from datetime import timedelta
import urllib.request, json 

DOMAIN = "smhiforecast"
ICON = 'mdi:weather-cloudy'
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=60)
_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'https://https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/#lon#/lat/#lat#/data.json'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required('longitude'): cv.string,
        vol.Required('latitude'): cv.string,
    }
)
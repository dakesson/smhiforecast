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
_RESOURCE = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/#lon#/lat/#lat#/data.json'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required('longitude'): cv.string,
        vol.Required('latitude'): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):

    capture = ['tcc_mean','lcc_mean','mcc_mean','hcc_mean','t', 'ws', 'r']
    lon = config.get('longitude')
    lat = config.get('latitude')
    if len(lon) > 0 and len(lat) > 0:
        smhiData = SMHIData(_RESOURCE.replace('#lon#', lon).replace('#lat#', lat))
        smhiData.update()
        for cloudType in capture:
            add_entities([SmhiForecastSensor(0, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(1, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(2, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(3, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(4, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(5, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(6, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(7, cloudType, smhiData)], True)
            add_entities([SmhiForecastSensor(8, cloudType, smhiData)], True)

class SMHIData:
    def __init__(self, url):
        self.url = url
        self.data = {}
        self.unit = ""

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        with urllib.request.urlopen(self.url) as url:
            data = json.loads(url.read().decode())
        self.data = data['timeSeries']
        

class SmhiForecastSensor(Entity):

    def __init__(self, timeStep, cloudType, smhiData):
        self.timeStep = timeStep
        self.cloudType = cloudType
        self.smhiData = smhiData
        self._attributes = {}

    @property
    def name(self):
        return 'Smhi forecast %s T%i' % (self.cloudType, self.timeStep)

    @property
    def state(self):

        self._attributes['validTime'] = self.smhiData.data[self.timeStep]['validTime']
        for value in self.smhiData.data[self.timeStep]['parameters']:
            self.unit = value['unit']
            if value['name'] == self.cloudType:
                return value['values'][0]
        return '-99'

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def unit_of_measurement(self):
        return self.unit

    def update(self):
        self.smhiData.update()

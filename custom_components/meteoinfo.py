import logging

import voluptuous as vol

REQUIREMENTS = ['pyquery==1.4.0']
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'meteoinfo'
CONF_CITY_CODE = "city_code"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({

    }),
}, extra=vol.ALLOW_EXTRA)

PLATFORM_SCHEMA = vol.Schema({
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the connection to the service."""
    return True

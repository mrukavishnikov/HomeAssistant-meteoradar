"""
Demo camera platform that has a fake camera.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
import logging

import voluptuous as vol
from homeassistant.components.camera import Camera
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

DEPENDENCIES = ['meteoinfo']
CONF_RADAR_CODE = "radar_code"

SUPPORT_ON_OFF = 1

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
}, extra=vol.ALLOW_EXTRA)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RADAR_CODE, default='UMMN'): cv.string,
    vol.Optional(CONF_NAME, default='Meteoradar'): cv.string,
})


async def async_setup_platform(hass, config, async_add_devices,
                               discovery_info=None):
    _LOGGER.info(config)

    code = config.get(CONF_RADAR_CODE)
    name = config.get(CONF_NAME)

    device = MeteoRadarCamera(name, code)

    if device is not None:
        async_add_devices([
            device
        ])


class MeteoRadarCamera(Camera):
    """The representation of a Demo camera."""

    def __init__(self, name, code):
        """Initialize demo camera component."""
        super().__init__()
        self._name = name
        self._url = "http://meteoinfo.by/radar/" + code + "/" + code + "_latest.png"
        self._motion_status = False
        self.is_streaming = True

    def camera_image(self):
        """Return a faked still image response."""
        import urllib.request
        with urllib.request.urlopen(self._url) as image:
            return image.read()

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def should_poll(self):
        """Demo camera doesn't need poll.
        Need explicitly call schedule_update_ha_state() after state changed.
        """
        return False

    @property
    def supported_features(self):
        """Camera support turn on/off features."""
        return SUPPORT_ON_OFF

    @property
    def is_on(self):
        """Whether camera is on (streaming)."""
        return self.is_streaming

    @property
    def motion_detection_enabled(self):
        """Camera Motion Detection Status."""
        return self._motion_status

    def enable_motion_detection(self):
        """Enable the Motion detection in base station (Arm)."""
        self._motion_status = True
        self.schedule_update_ha_state()

    def disable_motion_detection(self):
        """Disable the motion detection in base station (Disarm)."""
        self._motion_status = False
        self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off camera."""
        self.is_streaming = False
        self.schedule_update_ha_state()

    def turn_on(self):
        """Turn on camera."""
        self.is_streaming = True
        self.schedule_update_ha_state()

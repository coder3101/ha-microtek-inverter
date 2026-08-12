"""Constants and definitions for the Microtek Inverter integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorEntityDescription

DOMAIN = "microtek"
VERSION = "0.1.0"

PLATFORMS = ["sensor", "binary_sensor"]

API_BASE = "https://ndp8a9vu2a.execute-api.ap-south-1.amazonaws.com/prod"

DEFAULT_COUNTRY_CODE = "+91"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
LOGIN_EXPIRY_MS = 7200000  # 2 h, returned by the API

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_COUNTRY_CODE = "country_code"
CONF_HOME_ID = "home_id"
CONF_DEVICE_ID = "device_id"
CONF_SCAN_INTERVAL = "scan_interval"

USER_AGENT = "sebz/18 CFNetwork/3860.700.1 Darwin/25.6.0"

# String device_class / unit values are used instead of Home Assistant enums so
# the integration imports cleanly across many HA versions (the unit enums move
# and change between releases).
SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="involt",
        name="Input voltage",
        icon="mdi:transmission-tower",
        device_class="voltage",
        native_unit_of_measurement="V",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="outvolt",
        name="Output voltage",
        icon="mdi:home-lightning-bolt",
        device_class="voltage",
        native_unit_of_measurement="V",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="batvolt",
        name="Battery voltage",
        icon="mdi:battery",
        device_class="voltage",
        native_unit_of_measurement="V",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="chrgcurr",
        name="Charge current",
        icon="mdi:battery-charging-outline",
        device_class="current",
        native_unit_of_measurement="A",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="dischrgcurr",
        name="Discharge current",
        icon="mdi:battery-arrow-down-outline",
        device_class="current",
        native_unit_of_measurement="A",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="frequency",
        name="Frequency",
        icon="mdi:sine-wave",
        device_class="frequency",
        native_unit_of_measurement="Hz",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="load",
        name="Load",
        icon="mdi:gauge",
        native_unit_of_measurement="%",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="rssi",
        name="WiFi signal",
        icon="mdi:wifi",
        device_class="signal_strength",
        native_unit_of_measurement="dBm",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="chrgtime",
        name="Charge time",
        icon="mdi:timelapse",
        device_class="duration",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="bkptime",
        name="Backup time",
        icon="mdi:history",
        device_class="duration",
        state_class="measurement",
    ),
    SensorEntityDescription(
        key="mode",
        name="Inverter mode",
        icon="mdi:power-settings",
    ),
    SensorEntityDescription(
        key="chrgsts",
        name="Charge status",
        icon="mdi:battery-charging",
    ),
    SensorEntityDescription(
        key="battype",
        name="Battery type",
        icon="mdi:battery",
    ),
    SensorEntityDescription(
        key="mCoreVer",
        name="Core firmware",
        entity_registry_enabled_default=False,
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="fv",
        name="Firmware version",
        entity_registry_enabled_default=False,
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="flv",
        name="Flash version",
        entity_registry_enabled_default=False,
        icon="mdi:chip",
    ),
)

# 0/1 flags exposed as binary sensors (on = non-zero), with display icons.
BINARY_SENSORS: dict[str, str] = {
    "pow": "mdi:power",
    "ups": "mdi:power-plug",
    "mains": "mdi:power-plug-outline",
    "fan": "mdi:fan",
    "buzz": "mdi:bell",
    "highpwr": "mdi:rocket-launch",
    "vacation": "mdi:palm-tree",
    "mainscut": "mdi:power-plug-off",
    "turbochrgsts": "mdi:battery-charging-high",
    "activated": "mdi:check-decagram",
    "wConn": "mdi:wifi",
    "bConn": "mdi:bluetooth",
    "cbtripwarn": "mdi:alert",
    "wlevelwarn": "mdi:alert",
    "lowbatwarn": "mdi:battery-alert",
    "chrgrelay_flt": "mdi:alert",
    "outvolt_flt": "mdi:alert",
    "batvolt_flt": "mdi:battery-alert-variant",
    "backfeed_flt": "mdi:alert",
    "transF_temp_flt": "mdi:thermometer-alert",
    "mosfet_temp_flt": "mdi:thermometer-alert",
    "shrtckt_flt": "mdi:alert",
    "overload_flt": "mdi:alert",
}

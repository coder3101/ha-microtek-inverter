"""Constants and definitions for the Microtek Inverter integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfSignalStrength,
    UnitOfTime,
)

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

# Keys pulled from the `things[].state` object (nested, as returned by the API).
STATE_KEYS = [
    "rssi",
    "pow",
    "ups",
    "mode",
    "involt",
    "outvolt",
    "batvolt",
    "chrgcurr",
    "dischrgcurr",
    "load",
    "frequency",
    "chrgsts",
    "battype",
    "battypesel",
    "turbochrgsts",
    "chrgtime",
    "bkptime",
    "fan",
    "mains",
    "buzz",
    "highpwr",
    "vacation",
    "mainscut",
    "pSliderV",
    "bkpSliderV",
    "mCoreVer",
    "fv",
    "flv",
    "udid",
    "ts",
]

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="involt",
        name="Input voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="outvolt",
        name="Output voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="batvolt",
        name="Battery voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="chrgcurr",
        name="Charge current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="dischrgcurr",
        name="Discharge current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="frequency",
        name="Frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="load",
        name="Load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="rssi",
        name="WiFi signal",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=UnitOfSignalStrength.DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="chrgtime",
        name="Charge time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="bkptime",
        name="Backup time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
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

# 0/1 flags exposed as binary sensors (on = non-zero).
BINARY_SENSOR_KEYS = (
    "pow",
    "ups",
    "mains",
    "fan",
    "buzz",
    "highpwr",
    "vacation",
    "mainscut",
    "turbochrgsts",
    "activated",
    "wConn",
    "bConn",
    "cbtripwarn",
    "wlevelwarn",
    "lowbatwarn",
    "chrgrelay_flt",
    "outvolt_flt",
    "batvolt_flt",
    "backfeed_flt",
    "transF_temp_flt",
    "mosfet_temp_flt",
    "shrtckt_flt",
    "overload_flt",
)

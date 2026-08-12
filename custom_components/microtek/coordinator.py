"""Data coordinator for the Microtek Inverter integration."""

from __future__ import annotations

import json
import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_DEVICE_ID,
    CONF_HOME_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .microtek_client import MicrotekAuthError, MicrotekClient

_LOGGER = logging.getLogger(__name__)


class MicrotekDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch the inverter's live state from the Microtek cloud."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: MicrotekClient) -> None:
        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.total_seconds())
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.client = client
        self.home_id: str = entry.data[CONF_HOME_ID]
        self.device_id: str = entry.data[CONF_DEVICE_ID]

        self.udid: str | None = None
        self.model_name: str | None = None
        self.model_code: str | None = None
        self.serial_number: str | None = None
        self.ssid: str | None = None
        self.connected: bool | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            things = await self.client.get_things(self.home_id)
        except MicrotekAuthError as err:
            raise ConfigEntryAuthFailed from err
        except Exception as err:
            raise UpdateFailed(f"Failed to fetch inverter data: {err}") from err

        thing = next((t for t in things if t.get("id") == self.device_id), None)
        if thing is None and things:
            thing = things[0]
        if thing is None:
            raise UpdateFailed("Inverter not found for this home")

        self.udid = thing.get("id")
        self.model_name = thing.get("model_name")
        self.model_code = thing.get("model_code")
        self.ssid = thing.get("ssid")
        self.connected = bool(thing.get("connected"))

        user_config = json.loads(thing.get("user_config") or "{}")
        self.serial_number = user_config.get("serial_number")

        try:
            state = json.loads(thing.get("state") or "{}")
        except json.JSONDecodeError as err:
            raise UpdateFailed(f"Invalid state payload from cloud: {err}") from err

        return {
            "state": state,
            "connected": self.connected,
            "model_name": self.model_name,
            "model_code": self.model_code,
            "serial_number": self.serial_number,
            "ssid": self.ssid,
        }

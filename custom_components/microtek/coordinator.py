"""Data coordinator for the Microtek Inverter integration (AP data source)."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .ap_client import MicrotekAPClient, MicrotekAPError
from .const import (
    CONF_DEVICE_ID,
    CONF_MODEL_CODE,
    CONF_MODEL_NAME,
    CONF_SCAN_INTERVAL,
    CONF_SERIAL_NUMBER,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class MicrotekDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll the inverter's live state directly over its AP HTTP interface."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: MicrotekAPClient) -> None:
        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.total_seconds())
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.client = client
        self.device_id: str = entry.data[CONF_DEVICE_ID]
        self.model_name: str | None = entry.data.get(CONF_MODEL_NAME)
        self.model_code: str | None = entry.data.get(CONF_MODEL_CODE)
        self.serial_number: str | None = entry.data.get(CONF_SERIAL_NUMBER)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            state = await self.client.get_status()
        except MicrotekAPError as err:
            raise UpdateFailed(f"Failed to fetch inverter data: {err}") from err

        if not self.model_name:
            self.model_name = state.get("m_name")
        if not self.model_code:
            self.model_code = state.get("m_name")

        return {
            "state": state,
            "connected": bool(state.get("wConn")),
            "model_name": self.model_name,
            "model_code": self.model_code,
            "serial_number": self.serial_number,
            "ssid": state.get("udid"),
        }

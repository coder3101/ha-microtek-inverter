"""Select platform for the Microtek Inverter integration (AP write)."""

from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .ap_client import MicrotekAPError
from .const import DOMAIN, MODE_SELECT_OPTIONS
from .coordinator import MicrotekDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MicrotekDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MicrotekModeSelect(coordinator)])


class MicrotekModeSelect(CoordinatorEntity[MicrotekDataUpdateCoordinator], SelectEntity):
    """Select that writes the inverter ``mode`` field via ``POST /sds``."""

    _attr_has_entity_name = True
    _attr_name = "Inverter mode"
    _attr_icon = "mdi:power-settings"
    _attr_options = list(MODE_SELECT_OPTIONS.values())

    def __init__(self, coordinator: MicrotekDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_mode"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name="Microtek Inverter",
            manufacturer="Microtek",
            model=self.coordinator.model_name or self.coordinator.model_code,
        )

    @property
    def current_option(self) -> str | None:
        state = self.coordinator.data.get("state", {}) if self.coordinator.data else {}
        value = state.get("mode")
        if value is None:
            return None
        return MODE_SELECT_OPTIONS.get(int(value), str(value))

    async def async_select_option(self, option: str) -> None:
        mode = next(k for k, v in MODE_SELECT_OPTIONS.items() if v == option)
        try:
            await self.coordinator.client.set_field("mode", mode)
        except MicrotekAPError as err:
            _LOGGER.error("Failed to set mode=%s on inverter: %s", mode, err)
        await self.coordinator.async_refresh()

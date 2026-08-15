"""Switch platform for the Microtek Inverter integration (AP write)."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .ap_client import MicrotekAPError
from .const import DOMAIN, SWITCH_KEYS
from .coordinator import MicrotekDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# The inverter applies /sds writes with a short delay; refresh must wait long
# enough for the new value to appear in /gds, otherwise the stale pre-write
# value reverts the optimistic switch state.
WRITE_SETTLE_SECONDS = 6


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MicrotekDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(MicrotekSwitch(coordinator, key) for key in SWITCH_KEYS)


class MicrotekSwitch(CoordinatorEntity[MicrotekDataUpdateCoordinator], SwitchEntity):
    """Switch that writes a 0/1 flag to the inverter via ``POST /sds``."""

    def __init__(self, coordinator: MicrotekDataUpdateCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{coordinator.device_id}_{key}"
        self._attr_name = key.replace("_", " ").title()
        self._attr_icon = SWITCH_KEYS[key]

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name="Microtek Inverter",
            manufacturer="Microtek",
            model=self.coordinator.model_name or self.coordinator.model_code,
        )

    @property
    def is_on(self) -> bool | None:
        state = self.coordinator.data.get("state", {}) if self.coordinator.data else {}
        value = state.get(self._key)
        if value is None:
            return None
        return bool(int(value)) if str(value).lstrip("-").isdigit() else bool(value)

    async def async_turn_on(self, **kwargs) -> None:
        await self._async_set(1)

    async def async_turn_off(self, **kwargs) -> None:
        await self._async_set(0)

    async def _async_set(self, value: int) -> None:
        state = self.coordinator.data.setdefault("state", {})
        old = state.get(self._key)
        state[self._key] = value
        self.async_write_ha_state()
        try:
            await self.coordinator.client.set_field(self._key, value)
        except MicrotekAPError as err:
            _LOGGER.error("Failed to set %s=%s on inverter: %s", self._key, value, err)
            if old is not None:
                state[self._key] = old
            self.async_write_ha_state()
            return
        await asyncio.sleep(WRITE_SETTLE_SECONDS)
        await self.coordinator.async_refresh()

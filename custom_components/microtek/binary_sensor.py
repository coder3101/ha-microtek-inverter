"""Binary sensor platform for the Microtek Inverter integration (cloud read-only)."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import BINARY_SENSOR_KEYS, DOMAIN
from .coordinator import MicrotekDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MicrotekDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(MicrotekBinarySensor(coordinator, key) for key in BINARY_SENSOR_KEYS)


class MicrotekBinarySensor(CoordinatorEntity[MicrotekDataUpdateCoordinator], BinarySensorEntity):
    """Binary sensor for a 0/1 flag or fault in the inverter's live state."""

    def __init__(
        self,
        coordinator: MicrotekDataUpdateCoordinator,
        key: str,
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{coordinator.device_id}_{key}"
        self._attr_name = key.replace("_", " ").title()
        if key.endswith("_flt"):
            self._attr_device_class = "problem"
        elif key == "mains":
            self._attr_device_class = "power"
        elif key == "wConn":
            self._attr_device_class = "connectivity"

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

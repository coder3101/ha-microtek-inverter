"""Sensor platform for the Microtek Inverter integration (cloud read-only)."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, SENSOR_DESCRIPTIONS
from .coordinator import MicrotekDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MicrotekDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(MicrotekSensor(coordinator, desc) for desc in SENSOR_DESCRIPTIONS)


class MicrotekSensor(CoordinatorEntity[MicrotekDataUpdateCoordinator], SensorEntity):
    """Sensor reading a single field from the inverter's live state."""

    def __init__(
        self,
        coordinator: MicrotekDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{coordinator.device_id}_{description.key}"
        self._attr_icon = description.icon

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name="Microtek Inverter",
            manufacturer="Microtek",
            model=self.coordinator.model_name or self.coordinator.model_code,
            sw_version=self.coordinator.data.get("state", {}).get("mCoreVer"),
        )

    @property
    def native_value(self) -> str | float | int | None:
        state = self.coordinator.data.get("state", {}) if self.coordinator.data else {}
        return state.get(self.entity_description.key)

"""The Microtek Inverter integration."""

from __future__ import annotations

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_COUNTRY_CODE,
    CONF_DEVICE_ID,
    CONF_HOME_ID,
    CONF_USERNAME,
    DEFAULT_COUNTRY_CODE,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import MicrotekDataUpdateCoordinator
from .microtek_client import MicrotekClient

_SESSION_KEY = f"{DOMAIN}_sessions"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = aiohttp.ClientSession()
    client = MicrotekClient(
        session,
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.data.get(CONF_COUNTRY_CODE, DEFAULT_COUNTRY_CODE),
    )
    coordinator = MicrotekDataUpdateCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.data.setdefault(_SESSION_KEY, {})[entry.entry_id] = session

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        session = hass.data.get(_SESSION_KEY, {}).pop(entry.entry_id, None)
        if session is not None:
            await session.close()
        hass.data.setdefault(DOMAIN, {}).pop(entry.entry_id, None)
        if not hass.data.get(_SESSION_KEY):
            hass.data.pop(_SESSION_KEY, None)
    return unload_ok

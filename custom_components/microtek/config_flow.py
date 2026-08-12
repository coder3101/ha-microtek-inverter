"""Config flow for the Microtek Inverter integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_COUNTRY_CODE,
    CONF_DEVICE_ID,
    CONF_HOME_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_COUNTRY_CODE,
    DOMAIN,
)
from .microtek_client import MicrotekAuthError, MicrotekClient


async def _build_client(hass: HomeAssistant, data: dict[str, Any]) -> MicrotekClient | None:
    """Create and validate a client against the account credentials.

    The returned client owns an open session; the caller must close it
    (``await client.close()``) when done.
    """
    session = aiohttp.ClientSession()
    try:
        client = MicrotekClient(
            session,
            data[CONF_USERNAME],
            data[CONF_PASSWORD],
            data.get(CONF_COUNTRY_CODE, DEFAULT_COUNTRY_CODE),
        )
        await client.get_homes()
        return client
    except MicrotekAuthError:
        await session.close()
        return None
    except Exception:
        await session.close()
        return None


class MicrotekConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Microtek Inverter."""

    VERSION = 1

    def __init__(self) -> None:
        self._creds: dict[str, Any] = {}
        self._homes: list[dict[str, Any]] = []
        self._home_id: str | None = None
        self._things: list[dict[str, Any]] = []

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            self._creds = user_input
            client = await _build_client(self.hass, user_input)
            if client is None:
                errors["base"] = "cannot_connect"
            else:
                self._homes = await client.get_homes()
                await client.close()
                if not self._homes:
                    errors["base"] = "no_homes"
                else:
                    return await self.async_step_home()

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_COUNTRY_CODE, default=DEFAULT_COUNTRY_CODE): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_home(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            self._home_id = user_input[CONF_HOME_ID]
            client = await _build_client(self.hass, self._creds)
            if client is None:
                errors["base"] = "cannot_connect"
            else:
                self._things = await client.get_things(self._home_id)
                await client.close()
                if not self._things:
                    errors["base"] = "no_devices"
                else:
                    return await self.async_step_device()

        choices = {h["id"]: h.get("name", "Home") for h in self._homes}
        schema = vol.Schema({vol.Required(CONF_HOME_ID): vol.In(choices)})
        return self.async_show_form(step_id="home", data_schema=schema, errors=errors)

    async def async_step_device(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID]
            await self.async_set_unique_id(device_id, raise_on_progress=False)
            self._abort_if_unique_id_configured()

            data = {
                **self._creds,
                CONF_HOME_ID: self._home_id,
                CONF_DEVICE_ID: device_id,
            }
            return self.async_create_entry(
                title=f"Microtek Inverter ({device_id})", data=data
            )

        choices = {
            t["id"]: f"{t.get('model_name', 'Inverter')} ({t['id']})"
            for t in self._things
        }
        schema = vol.Schema({vol.Required(CONF_DEVICE_ID): vol.In(choices)})
        return self.async_show_form(step_id="device", data_schema=schema, errors=errors)


class MicrotekOptionsFlow(config_entries.OptionsFlow):
    """Options flow for the Microtek Inverter integration."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, 60),
                ): int
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

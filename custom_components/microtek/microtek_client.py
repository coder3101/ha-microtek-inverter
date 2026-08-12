"""Async client for the Microtek cloud API."""

from __future__ import annotations

import json
import time
from typing import Any

import aiohttp

from .const import API_BASE, LOGIN_EXPIRY_MS, USER_AGENT


class MicrotekAuthError(Exception):
    """Raised when authentication fails (bad credentials or rejected token)."""


class MicrotekAPIError(Exception):
    """Raised for connection or server errors."""


class MicrotekClient:
    """Minimal async client for the Microtek/Sebz cloud API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
        country_code: str = "+91",
    ) -> None:
        self._session = session
        self._username = username
        self._password = password
        self._country_code = country_code
        self._token: str | None = None
        self._expires_at: float = 0.0

    async def _request(
        self, method: str, path: str, body: dict[str, Any] | None = None, auth: bool = False
    ) -> Any:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }
        if auth:
            if self._token is None or time.time() + 60 > self._expires_at:
                await self.login()
            headers["Authorization"] = f"Bearer {self._token}"

        kwargs: dict[str, Any] = {"headers": headers}
        if body is not None:
            kwargs["data"] = json.dumps(body)

        async with self._session.request(method, f"{API_BASE}{path}", **kwargs) as resp:
            text = await resp.text()
            if resp.status in (401, 403):
                self._token = None
                raise MicrotekAuthError(f"Unauthorized ({resp.status})")
            if resp.status >= 400:
                raise MicrotekAPIError(f"HTTP {resp.status}: {text}")
            return json.loads(text) if text else {}

    async def login(self) -> None:
        """Mint a fresh JWT from the account password."""
        body = {
            "country_code": self._country_code,
            "auth_id": self._username,
            "data": {"via": 1, "value": self._password},
        }
        data = await self._request("POST", "/auth/login", body=body)
        self._token = data.get("access_token")
        if not self._token:
            raise MicrotekAuthError("No access_token returned")
        expires_ms = data.get("expires_in", LOGIN_EXPIRY_MS)
        self._expires_at = time.time() + (expires_ms / 1000)

    async def get_homes(self) -> list[dict[str, Any]]:
        """Return the list of homes for the logged-in account."""
        data = await self._request("GET", "/user/homes", auth=True)
        return data.get("homes", [])

    async def get_things(self, home_id: str) -> list[dict[str, Any]]:
        """Return devices (things) under a home, including their live state."""
        data = await self._request("GET", f"/things?home_id={home_id}", auth=True)
        return data.get("things", [])

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        await self._session.close()

"""Async client for the inverter's direct AP mode HTTP API."""

from __future__ import annotations

import json
import time
from typing import Any

import aiohttp

from .const import USER_AGENT


class MicrotekAPError(Exception):
    """Raised when the AP endpoint returns an error or is unreachable."""


class MicrotekAPClient:
    """Direct HTTP client for the Microtek/Sebz inverter AP (`/gds`, `/sds`)."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        uat: str,
        host: str,
        port: int = 80,
    ) -> None:
        self._session = session
        self._uat = uat
        self._base = f"http://{host}:{port}"

    async def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        headers = {"User-Agent": USER_AGENT}
        kwargs: dict[str, Any] = {"headers": headers}
        if body is not None:
            kwargs["data"] = json.dumps(body)
            headers["Content-Type"] = "application/json"

        try:
            async with self._session.request(
                method, f"{self._base}{path}", timeout=aiohttp.ClientTimeout(total=5), **kwargs
            ) as resp:
                text = await resp.text()
        except aiohttp.ClientError as err:
            raise MicrotekAPError(f"Unreachable: {err}") from err
        except TimeoutError as err:
            raise MicrotekAPError("Request timed out") from err

        if resp.status != 200:
            raise MicrotekAPError(f"HTTP {resp.status}: {text[:200]}")
        return json.loads(text) if text else {}

    async def get_status(self) -> dict[str, Any]:
        """Read the full live status object via ``GET /gds``."""
        return await self._request("GET", f"/gds?uat={self._uat}")

    async def set_field(self, key: str, value: str | int | float) -> dict[str, Any]:
        """Set a parameter on the device via ``POST /sds``."""
        payload = {"uat": self._uat, "ts": int(time.time() * 1000), key: value}
        return await self._request("POST", "/sds", body=payload)

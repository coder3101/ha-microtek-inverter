# Home Assistant Integration for Microtek Inverters

> [!IMPORTANT]
> This is an **unofficial, community** integration. It is a fan project and is not
> affiliated with or endorsed by Microtek.

*Integration for Microtek **`SEBZ`** hybrid battery/UPS inverters (WiFi-equipped).*

This integration reads the live status of your inverter from the **Microtek
cloud**, so it works from any network — it does not need to be on the inverter's
local Wi-Fi.

![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)

## Features

- **Live sensors** — input/output/battery voltage, charge & discharge current,
  frequency, load %, WiFi signal (RSSI), charge & backup time, inverter mode,
  charge status, battery type, firmware versions.
- **Binary sensors** — mains present, UPS, fan, buzzer, WiFi/BT connection, and
  all fault/overload flags (low battery, overload, short circuit, over/under
  voltage, thermal, etc.).

> **Read-only.** This integration monitors only. It does **not** write or control
> the inverter.

## Tested on

- Microtek SEBZ Inverter (WiFi module, firmware `0007`)

## Installation

### Method 1: Using [HACS](https://hacs.xyz)

1. Open your Home Assistant UI.
2. Go to **HACS** → three dots (top right) → **Custom repositories**.
3. Under *Add custom repository*, enter:
   - **URL:** `https://github.com/coder3101/ha-microtek-inverter`
   - **Category:** Integration
4. Click **Add**.
5. Search for **Microtek** in HACS and select it.
6. Click **Install** and follow the prompts.

### Method 2: Manual Installation

1. Open the folder that holds your HA configuration (`configuration.yaml`).
2. Create a `custom_components` folder if it does not exist.
3. Create a folder called `microtek` inside it.
4. Download all files from `custom_components/microtek/` from this repository.
5. Place them in that folder.
6. Restart Home Assistant.

## Configuration

1. Open **Settings → Devices & Services → + Add Integration → Microtek Inverter**.
2. Enter your vendor app credentials:
   - **Username:** phone number used with the app.
   - **Password:** the app password.
   - **Country code:** e.g. `+91` (used for the phone number).
3. Select your **home**, then your **device**.
4. Done — sensor entities appear under the inverter device.

The polling interval can be changed in the integration's **Options** (default 60 s).

## Data source

The integration uses the Microtek cloud REST API:
oauth-style login (`/prod/auth/login`) returns a short-lived token, and the live
state is read from `/prod/things?home_id=...` (the `state` payload). The token is
renewed automatically.

> Third-party access to a building's inverter cloud API may violate the
> manufacturer's terms of service. Use only with accounts/devices you own.

## Caveats

- The integration reads state via `cloud_polling`; sensor updates appear at the
  configured interval, not in real time.
- No remote control is implemented (read-only by design).

## Logs

Enable debug logging in Home Assistant:

```yaml
logger:
  default: warning
  logs:
    custom_components.microtek: debug
```

## License

Apache-2.0

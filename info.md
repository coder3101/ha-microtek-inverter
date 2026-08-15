# Microtek Inverter

Community Home Assistant integration for **Microtek `SEBZ` hybrid battery/UPS
inverters** (WiFi modules). Reads live status **directly from the inverter's AP**
(`local_polling`) and supports control via switches/select. The cloud account is
used once during setup to fetch the device token.

## Features
- Live sensors: input/output/battery voltage, charge & discharge current,
  frequency, load %, WiFi signal, charge/backup time, inverter & charge status,
  firmware versions.
- Binary sensors: mains present, UPS, fan, buzzer, WiFi/BT connection, and all
  fault/overload flags.
- Switches: toggle inverter flags (UPS mode, buzzer, high power, vacation,
  mains cutoff, power on).
- Select: choose the inverter `mode`.

## Installation
**HACS:** add as a custom repository → category **Integration**.

**Manual:** copy `custom_components/microtek` into `config/custom_components/` and restart.

## Configuration
Add the integration → **Settings → Devices & Services → Microtek Inverter**, then
enter your vendor app credentials (phone number + password and country code).
Pick your home and device, optionally adjust the AP host/port (defaults
`192.168.4.1:80`), and confirm the device is reachable from HA. Poll interval
configurable in Options.

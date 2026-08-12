# Microtek Inverter

Community Home Assistant integration for **Microtek `SEBZ` hybrid battery/UPS
inverters** (WiFi modules). Reads live status from the Microtek cloud
(`cloud_polling`) — no need to be near the inverter.

> Read-only. This integration monitors inverter state but does not control it.

## Features
- Live sensors: input/output/battery voltage, charge & discharge current,
  frequency, load %, WiFi signal, charge/backup time, inverter & charge status,
  firmware versions.
- Binary sensors: mains present, UPS, fan, buzzer, WiFi/BT connection, and all
  fault/overload flags.

## Installation
**HACS:** add as a custom repository → category **Integration**.

**Manual:** copy `custom_components/microtek` into `config/custom_components/` and restart.

## Configuration
Add the integration → **Settings → Devices & Services → Microtek Inverter**, then
enter your vendor app credentials (phone number + password and country code).
Pick your home and device. Poll interval configurable in Options.

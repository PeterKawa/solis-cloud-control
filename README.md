# Solis Cloud Control Integration

[![CI](https://github.com/mkuthan/solis-cloud-control/actions/workflows/ci.yml/badge.svg)](https://github.com/mkuthan/solis-cloud-control/actions/workflows/ci.yml)
![GitHub Release](https://img.shields.io/github/v/release/mkuthan/solis-cloud-control)

This is the Solis Cloud Control API integration for Home Assistant.
It allows you to read and control various settings of your Solis inverter.

> [!NOTE]
> If your primary goal is to monitor data from the Solis Cloud Monitoring API, you might want to explore the [Solis Sensor Integration](https://github.com/hultenvp/solis-sensor/).  
> Both integrations are complementary and can be used together to enhance your Home Assistant setup.

## Installation

The integration is not currently available in [HACS](https://www.hacs.xyz/). However, you can install it manually by adding [custom repository](https://www.hacs.xyz/docs/faq/custom_repositories/).

> [!TIP]
> For updates on HACS availability, see [issue #7](https://github.com/mkuthan/solis-cloud-control/issues/7).

## Configuration

Configure Solis Cloud Control integration with:

* Solis API key
* Solis Token
* Solis Inverter Serial Number

## Features

* ⚡ Control storage modes: "Self-Use", "Feed-In Priority" and "Off-Grid"
* ⏱️ Schedule charge and discharge slots
* ⚖️ Set maximum export power
* 🛠️ Access "Battery Reserve" and "Allow Grid Charging" options as Storage Mode attributes

![Inverter Controls](inverter_controls.png)

It also provides battery related sensors:

![Inverter Sensors](inverter_sensors.png)

The integration also meets several non-functional requirements:

* 📦 Batch reading of all inverter settings in a single request to fit within the Solis Cloud API limits
* 🔄 Retry logic for API requests to mitigate API stability issues
* 🏡 Best Home Assistant practices for integration development 😜

## Local Development

Install dependencies (once):

```bash
uv sync
```

Run the integration locally:

```bash
./scripts/run
```

## Release

To release a new version, create a new tag and push it to the repository:

```bash
git tag v1.0.1
git push origin v1.0.1
```

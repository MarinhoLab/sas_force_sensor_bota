# sas_force_sensor_bota

> [!TIP]
> Repository for this package: https://github.com/MarinhoLab/sas_force_sensor_bota \
> More information about SmartArmStack is available in https://smartarmstack.github.io/.

[Bota Systems](https://botasystems.com) package compliant with `sas`. 

## Quick start

Docker examples that do not need any installation or cloning the repository.

### EtherCat

See `config/ethercat_gen0.json` for the example configuration file.

```console
mkdir -p ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
cd ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_force_sensor_bota/refs/heads/jazzy/docker/demo/compose_ethercat.yml

xhost +local:root
docker compose -f compose_ethercat.yml up
```

### Serial Communication

See `config/bota_binary_gen0.json` for the example configuration file.

```console
mkdir -p ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
cd ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_force_sensor_bota/refs/heads/jazzy/docker/demo/compose.yml

xhost +local:root
docker compose up
```

## Pre-requisites

```console
wget https://raw.githubusercontent.com/MarinhoLab/sas_force_sensor_bota/refs/heads/jazzy/docker/install.sh
chmod +x install.sh && . install.sh
```

## Running sensor server

```console
ros2 launch sas_force_sensor_bota force_sensor_launch.py
```

The launch file loads the parameters from `config/config.yaml` (override with
`config_file:=/path/to/config.yaml`). The hardware-specific JSON configuration
(`configuration_file_path`) is embedded in the YAML file: `config/config.yaml`
points at `bota_binary_gen0.json` and `config/config_ethercat.yaml` points at
`ethercat_gen0.json` (for the EtherCAT hardware).

| Configurable Parameter | Meaning |
|------------------------|---------|
| `config_file` (launch argument) | Path to the YAML configuration file. Defaults to `config/config.yaml`; use `config_ethercat.yaml` for the EtherCAT hardware. |

## ROS 2 Nodes & Parameters

### Node: `sas_force_sensor_bota_node`

| Property | Value |
|---|---|
| **Executable** | `sas_force_sensor_bota_node` |
| **ROS node name** | `sas_force_sensor_bota_node` (set by the `name` launch argument of `force_sensor_launch.py`) |
| **Description** | Reads the Bota force/torque sensor, publishes the wrench on `<topic_name>/get/wrench`, and keeps the sensor configured/activated for the node lifetime. |

#### Parameters

| Parameter | Type | Mandatory / Optional | Default | Purpose |
|---|---|---|---|---|
| `topic_name` | string | Optional | `/sas_force_sensor_bota` | Topic prefix; e.g. when there are multiple sensors in the same `ROS_DOMAIN` |
| `configuration_file_path` | string | Optional | in-code default pointing at `config/bota_binary_gen0.json` in the package share directory | Path to the Bota JSON configuration file (hardware-specific). May be given as an absolute path or as a filename relative to the package `config/` directory (as in the sample YAML files) |
| `sampling_time` | double | Optional | `0.01` | Sampling period of the read loop, in seconds |

**How mandatory/optional is determined in code:**
- **Mandatory** params are declared without a default — the node fails if they are not provided.
- **Optional** params are declared with an in-code default.

#### Sample launch

```console
ros2 launch sas_force_sensor_bota force_sensor_launch.py
```

To use the EtherCAT JSON configuration (select the EtherCAT YAML, which
embeds `configuration_file_path: ethercat_gen0.json`):

```console
ros2 launch sas_force_sensor_bota force_sensor_launch.py config_file:=$(ros2 pkg prefix sas_force_sensor_bota --share)/config/config_ethercat.yaml
```

## Example client

```console
ros2 run sas_force_sensor_bota sas_force_sensor_client_example_node
```

# sas_force_sensor_bota

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
ros2 launch sas_force_sensor_bota sas_force_sensor_bota_launch.py
```

| Configurable Parameter | Meaning |
|------------------------|---------|
|`topic_name`| Topic prefix, for instance, if there are multiple sensors in the same `ROS_DOMAIN`.|
|`configuration_file_path`| The path to the `json` configuration file, see examples in the `config` folder.|

## Example client

```console
ros2 run sas_force_sensor_bota sas_force_sensor_client_example_node
```

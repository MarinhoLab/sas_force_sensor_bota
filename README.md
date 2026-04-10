# sas_force_sensor_bota

## Quick start

```console
mkdir -p ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
cd ~/sas_tutorial_workspace/docker/sas_force_sensor_bota/demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_force_sensor_bota/refs/heads/main/docker/demo/compose.yml

xhost +local:root
docker compose up
```

## Pre-requisites

```console
python3 -m pip install bota_driver PyQt6 --break-system-packages
```

## Running sensor server

```console
ros2 launch sas_force_sensor_bota sas_force_sensor_bota_launch.py
```

## Example client

```console
ros2 run sas_force_sensor_bota sas_force_sensor_client_example_node
```

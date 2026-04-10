# sas_force_sensor_bota

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
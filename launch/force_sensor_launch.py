# Copyright (c) 2012-2026 Murilo Marques Marinho
#
#    This file is part of sas_force_sensor_bota.
#
#    sas_force_sensor_bota is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_force_sensor_bota is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_force_sensor_bota.  If not, see <https://www.gnu.org/licenses/>.

import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Launch the Bota force sensor node.

    Parameters are loaded from a YAML configuration file. Pass a different
    file with ``config_file:=/path/to/config.yaml`` (e.g.
    ``config_ethercat.yaml`` for the EtherCAT hardware). The
    hardware-specific ``configuration_file_path`` (a JSON file in ``config/``)
    is embedded in the YAML configuration file.
    """
    name = LaunchConfiguration('name')
    config_file = LaunchConfiguration('config_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'name',
            default_value='sas_force_sensor_bota_node'
        ),
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_force_sensor_bota'), 'config', 'config.yaml')
        ),
        Node(
            package='sas_force_sensor_bota',
            executable='sas_force_sensor_bota_node',
            output='screen',
            emulate_tty=True,
            name=name,
            parameters=[config_file]
        )
    ])

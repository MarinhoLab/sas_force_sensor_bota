import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Launch the Bota force sensor node.

    Parameters are loaded from a YAML configuration file. Pass a different
    file with ``config_file:=/path/to/config.yaml``.
    The hardware-specific ``configuration_file_path`` (a JSON file, see the
    examples in ``config/``) is provided as a launch argument.
    """
    name = LaunchConfiguration('name')
    config_file = LaunchConfiguration('config_file')
    configuration_file_path = LaunchConfiguration('configuration_file_path')

    return LaunchDescription([
        DeclareLaunchArgument(
            'name',
            default_value='sas_force_sensor_bota_node'
        ),
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_force_sensor_bota'), 'config', 'config.yaml')
        ),
        DeclareLaunchArgument(
            'configuration_file_path',
            default_value=os.path.join(get_package_share_directory('sas_force_sensor_bota'), 'config', 'bota_binary_gen0.json')
        ),
        Node(
            package='sas_force_sensor_bota',
            executable='sas_force_sensor_bota_node',
            output='screen',
            emulate_tty=True,
            name=name,
            parameters=[
                config_file,
                {'configuration_file_path': configuration_file_path}
            ]
        )
    ])

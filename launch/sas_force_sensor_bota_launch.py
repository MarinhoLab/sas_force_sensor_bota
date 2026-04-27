import pathlib
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    topic_name = LaunchConfiguration('topic_name')

    configuration_file_path = LaunchConfiguration('configuration_file_path')
    this_package_share_directory = get_package_share_directory('sas_force_sensor_bota')
    default_configuration_file_path = str(this_package_share_directory / pathlib.Path("config") / pathlib.Path(
        "../config/bota_binary_gen0.json"))

    return LaunchDescription([
        DeclareLaunchArgument(
            'topic_name',
            default_value='/sas_force_sensor_bota',
        ),
        DeclareLaunchArgument(
            'configuration_file_path',
            default_value=default_configuration_file_path
        ),
        Node(
            package='sas_force_sensor_bota',
            executable='sas_force_sensor_bota_node',
            output='screen',
            emulate_tty=True,
            name='sas_force_sensor_bota_node',
            parameters=[{
                "topic_name": topic_name,
                "configuration_file_path": configuration_file_path,
            }]
        )
    ])

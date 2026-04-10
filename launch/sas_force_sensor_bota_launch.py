from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='sas_force_sensor_bota',
            executable='sas_force_sensor_bota_node',
            output='screen',
            emulate_tty=True,
            name='sas_force_sensor_bota_node',
            parameters=[{
            }]
        )

    ])

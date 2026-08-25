"""
Copyright (C) 2020-2026 Murilo Marques Marinho (www.murilomarinho.info)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>.
"""
import os.path
import pathlib
import bota_driver

from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import WrenchStamped

from sas_core import Clock

class ForceSensorBota(Node):
    def __init__(self):
        super().__init__('sas_force_sensor_bota')

        self.declare_parameter('topic_name', '/sas_force_sensor_bota')
        self.topic_name = self.get_parameter('topic_name').get_parameter_value().string_value

        this_package_share_directory = get_package_share_directory('sas_force_sensor_bota')
        default_configuration_file_path = str(this_package_share_directory / pathlib.Path("config") / pathlib.Path(
            "bota_binary_gen0.json"))

        self.declare_parameter('configuration_file_path', default_configuration_file_path)
        configuration_file_path = self.get_parameter('configuration_file_path').get_parameter_value().string_value

        # A path relative to the package config/ directory (as in the sample
        # YAML configurations) is resolved against that directory. Absolute
        # paths are used as given.
        if not os.path.isabs(configuration_file_path):
            configuration_file_path = str(this_package_share_directory / pathlib.Path("config") / pathlib.Path(
                configuration_file_path))

        self.declare_parameter('sampling_time', 0.01)
        sampling_time = self.get_parameter('sampling_time').get_parameter_value().double_value

        self.publisher = self.create_publisher(
            msg_type=WrenchStamped,
            topic=f'{self.topic_name}/get/wrench',
            qos_profile=1)

        self.running = False
        self.bota_ft_sensor_driver = bota_driver.BotaDriver(configuration_file_path)

        if not self.bota_ft_sensor_driver.configure():
            raise RuntimeError("Failed to configure driver")

        if not self.bota_ft_sensor_driver.tare():
            raise RuntimeError("Failed to tare sensor")

        if not self.bota_ft_sensor_driver.activate():
            raise RuntimeError("Failed to activate driver")

        self.clock = Clock(sampling_time)
        self.clock.init()
        self.running = True

    def is_open(self):
        return self.running

    def read(self):
        """
        Extract the data from the bota_frame
        status = bota_frame.status
        force = bota_frame.force
        torque = bota_frame.torque
        timestamp = bota_frame.timestamp
        temperature = bota_frame.temperature
        acceleration = bota_frame.acceleration
        angular_rate = bota_frame.angular_rate
        :return:
        """
        if not self.running:
            return None

        self.clock.update_and_sleep()

        # April 27, 2026. Some sensors are not compatible with blocking reads.
        # bota_frame = self.bota_ft_sensor_driver.read_frame_blocking()
        bota_frame = self.bota_ft_sensor_driver.read_frame()

        ws = WrenchStamped()

        ws.header.stamp = self.get_clock().now().to_msg()
        ws.header.frame_id = self.topic_name
        ws.wrench.force.x = bota_frame.force[0]
        ws.wrench.force.y = bota_frame.force[1]
        ws.wrench.force.z = bota_frame.force[2]
        ws.wrench.torque.x = bota_frame.torque[0]
        ws.wrench.torque.y = bota_frame.torque[1]
        ws.wrench.torque.z = bota_frame.torque[2]

        self.publisher.publish(ws)

        return bota_frame

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if not self.bota_ft_sensor_driver.deactivate():
            raise RuntimeError("Failed to deactivate driver")

        if not self.bota_ft_sensor_driver.shutdown():
            raise RuntimeError("Failed to shutdown driver")



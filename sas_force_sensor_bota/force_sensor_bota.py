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
import bota_driver
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped

class ForceSensorBota(Node):
    def __init__(self, config_file: str):
        super().__init__('sas_force_sensor_bota')

        self.publisher = self.create_publisher(
            msg_type=WrenchStamped,
            topic='/sas_patient_side_manager/m0_0/set/external_mapped_wrench',
            qos_profile=1)

        self.running = False
        self.bota_ft_sensor_driver = bota_driver.BotaDriver(config_file)

        # Transition driver from UNCONFIGURED to INACTIVE state
        if not self.bota_ft_sensor_driver.configure():
            raise RuntimeError("Failed to configure driver")

        # Uncomment to tare the sensor
        if not self.bota_ft_sensor_driver.tare():
            raise RuntimeError("Failed to tare sensor")

        # Transition driver from INACTIVE to ACTIVE state
        if not self.bota_ft_sensor_driver.activate():
            raise RuntimeError("Failed to activate driver")

        self.running = True

    def is_open(self):
        return self.running

    def read(self):
        if not self.running:
            return None

        bota_frame = self.bota_ft_sensor_driver.read_frame_blocking()

        ws = WrenchStamped()

        ws.header.stamp = self.get_clock().now().to_msg()
        ws.header.frame_id = 'sas_force_sensor_bota'

        a = 0.00015

        ws.wrench.force.x = -bota_frame.force[0]*a
        ws.wrench.force.y = -bota_frame.force[1]*a
        ws.wrench.force.z = 2*bota_frame.force[2]*a

        self.publisher.publish(ws)

        return bota_frame

        # Extract the data from the bota_frame
        #status = bota_frame.status
        #force = bota_frame.force
        #torque = bota_frame.torque
        #timestamp = bota_frame.timestamp
        #temperature = bota_frame.temperature
        #acceleration = bota_frame.acceleration
        #angular_rate = bota_frame.angular_rate

        #################################
        ## YOUR CONTROL LOOP CODE HERE ##
        #################################

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Transition driver from ACTIVE to INACTIVE state
        if not self.bota_ft_sensor_driver.deactivate():
            raise RuntimeError("Failed to deactivate driver")

        # Shutdown the driver
        if not self.bota_ft_sensor_driver.shutdown():
            raise RuntimeError("Failed to shutdown driver")



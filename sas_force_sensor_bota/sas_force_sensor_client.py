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
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped

class ForceSensorClient:
    def __init__(self, node, topic_prefix):
        self.topic_prefix = topic_prefix
        self.node = node

        self.subscriber = self.node.create_subscription(
            msg_type=WrenchStamped,
            topic=f'{topic_prefix}/get/wrench',
            callback=self.subscriber_callback,
            qos_profile=1)

        self.wrench = None

    def subscriber_callback(self, msg: WrenchStamped) -> np.array:
        self.wrench = np.array([msg.force.x, msg.force.y, msg.force.z, msg.torque.x, msg.torque.y, msg.torque.z])

    def get_wrench(self):
        if self.wrench is None:
            raise Exception("Trying to get wrench but not initialised yet.")
        return self.wrench

    def is_enabled(self):
        return self.wrench is not None

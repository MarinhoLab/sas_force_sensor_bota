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
import time
import rclpy
from rclpy.node import Node
from sas_force_sensor_bota.sas_force_sensor_client import ForceSensorClient

def main(args=None):
    try:
        rclpy.init(args=args)

        node = Node('sas_force_sensor_bota_client_example')

        fsc = ForceSensorClient(node,"/sas_force_sensor_bota")

        while not fsc.is_enabled():
            print("Waiting for interface to be available...")
            time.sleep(1)
            rclpy.spin_once(node)

        while True:
            print(f"Wrench = {fsc.get_wrench()}")
            rclpy.spin_once(node)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
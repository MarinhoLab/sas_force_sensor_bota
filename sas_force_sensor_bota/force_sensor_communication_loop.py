#!/usr/bin/env python
"""
Copyright (C) 2020-2025 Murilo Marques Marinho (www.murilomarinho.info)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>.
"""
import rclpy
from ament_index_python.packages import get_package_share_directory

import multiprocessing as mp
import multiprocessing.managers as mm
import time

from sas_force_sensor_bota.shared_memory.server import ForceSensorSharedMemoryServer
from sas_force_sensor_bota.shared_memory.client import ForceSensorSharedMemoryClient
from sas_force_sensor_bota.force_sensor_bota import ForceSensorBota

import pathlib

def communication_loop(run):
    rclpy.init()

    this_package_share_directory = get_package_share_directory('sas_force_sensor_bota')

    # TODO make this configurable
    config_path = str(this_package_share_directory / pathlib.Path("config") / pathlib.Path(
        "../config/bota_binary_gen0.json"))

    with ForceSensorBota(config_path) as fsb, mm.SharedMemoryManager() as smm:

        lock = mp.Lock()

        shared_memory_server = ForceSensorSharedMemoryServer(shared_memory_manager=smm, lock=lock)

        shared_memory_receiver_process = mp.Process(
            target=run,
            args=(shared_memory_server.get_shared_memory_receiver_initializer_args(), lock)
        )

        shared_memory_receiver_process.start()

        try:
            # Control loop
            while True:
                # If connection is open, update, handle q and qd
                if fsb.is_open():
                    frame = fsb.read()
                    f = frame.force
                    t = frame.torque
                    shared_memory_server.send_wrench(f + t)
                    #rclpy.spin_once(fsb)

                # Always send connection status
                shared_memory_server.send_is_open(fsb.is_open())

                # Check if shutdown signal was sent by receiver
                if shared_memory_server.get_shutdown_flag():
                    print('force_sensor_bota::__main__::Info::Server shutdown by client.')
                    break

        except Exception as e:
            print('force_sensor_bota::__main__::Error::' + str(e))
        except KeyboardInterrupt:
            print('force_sensor_bota::__main__::Info::Shutdown by CTRL+C.')
            shared_memory_server.send_shutdown_flag(True)
        shared_memory_receiver_process.join()

def run(shared_memory_info, lock):
    shared_memory_client = ForceSensorSharedMemoryClient(shared_memory_info, lock)

    try:
        while True:
            time.sleep(1)
            if shared_memory_client.is_open():
                print(shared_memory_client.get_wrench())
    except Exception as e:
        print("umirobot_main_window::run::Error::" + str(e))
    except KeyboardInterrupt:
        print("umirobot_main_window::run::Info::Interrupted by user.")

    shared_memory_client.send_shutdown_flag(True)
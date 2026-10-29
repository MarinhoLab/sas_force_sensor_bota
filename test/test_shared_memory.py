# Copyright (c) 2020-2026 Murilo Marques Marinho
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
"""Tests for the shared-memory force sensor server/client pair."""

import multiprocessing as mp
import multiprocessing.managers as mm

import pytest
from sas_force_sensor_bota.shared_memory.client import ForceSensorSharedMemoryClient
from sas_force_sensor_bota.shared_memory.server import ForceSensorSharedMemoryServer


def test_shared_memory_server_client_round_trip():
    lock = mp.Lock()
    with mm.SharedMemoryManager() as smm:
        server = ForceSensorSharedMemoryServer(shared_memory_manager=smm, lock=lock)
        client = ForceSensorSharedMemoryClient(
            server.get_shared_memory_receiver_initializer_args(), lock)

        assert client.get_wrench() == [None] * 6
        assert not client.is_open()

        server.send_is_open(True)
        assert client.is_open()

        wrench = [1.0, -2.0, 3.0, -4.0, 5.0, -6.0]
        server.send_wrench(wrench)
        assert client.get_wrench() == pytest.approx(wrench)

        # Malformed payloads are ignored.
        server.send_wrench([1.0])
        server.send_wrench(None)
        assert client.get_wrench() == pytest.approx(wrench)

        assert not client.get_shutdown_flag()
        client.send_shutdown_flag(True)
        assert server.get_shutdown_flag()

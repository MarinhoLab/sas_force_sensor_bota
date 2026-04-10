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
from PyQt6.QtCore import QTimer, Qt, QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QLabel

from sas_force_sensor_bota.shared_memory.client import ForceSensorSharedMemoryClient

class ForceSensorMainWindow(QMainWindow):
    def __init__(self, shared_memory_client: ForceSensorSharedMemoryClient):
        super().__init__()

        self.setWindowTitle("Force Reader")

        self.setMinimumHeight(400)

        self.shared_memory_client: ForceSensorSharedMemoryClient = shared_memory_client

        self.timer_ = QTimer()
        self.timer_.timeout.connect(self._timer_callback)
        self.timer_.start(1)

        self.layout = QVBoxLayout(self)

        self.slider_force_label = QLabel(self)
        self.slider_force_label.setText("Force")
        self.slider_torque_label = QLabel(self)
        self.slider_torque_label.setText("Torque")

        self.slider_force = QSlider(Qt.Orientation.Vertical, self)
        self.slider_force.setRange(-300, 300)
        self.slider_torque = QSlider(Qt.Orientation.Vertical, self)
        self.slider_torque.setRange(-300, 300)

        self.layout.addWidget(self.slider_force_label)
        self.layout.addWidget(self.slider_force)
        self.layout.addWidget(self.slider_torque)

        self.setCentralWidget(self.slider_force)


    def _timer_callback(self):
        try:
            if self.shared_memory_client.is_open():
                wrench = self.shared_memory_client.get_wrench()

                f = np.array(wrench[0:3])
                f_norm = np.linalg.norm(f)
                self.slider_force.setValue(int(f_norm))
                self.slider_force_label.setText('{:.2f}'.format(f_norm))

                t = np.array(wrench[3:5])
                t_norm = np.linalg.norm(t)
                self.slider_torque.setValue(int(t_norm))
                self.slider_torque_label.setText('{:.2f}'.format(t_norm))

            if self.shared_memory_client.get_shutdown_flag():
                QCoreApplication.quit()
        except ...:
            pass

def run(shared_memory_info, lock):
    shared_memory_client = ForceSensorSharedMemoryClient(shared_memory_info, lock)
    try:
        app = QApplication([])
        myapp = ForceSensorMainWindow(shared_memory_client)
        myapp.show()
        app.exec()
    except Exception as e:
        print("umirobot_main_window::run::Error::" + str(e))
    except KeyboardInterrupt:
        print("umirobot_main_window::run::Info::Interrupted by user.")

    shared_memory_client.send_shutdown_flag(True)
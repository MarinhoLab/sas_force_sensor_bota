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
from queue import Queue

import numpy as np

from PyQt6.QtCore import QTimer, Qt, QCoreApplication
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QSlider, QHBoxLayout, QVBoxLayout, QLabel

import pyqtgraph as pg

from sas_force_sensor_bota.shared_memory.client import ForceSensorSharedMemoryClient

class SliderLabelVertical(QWidget):
    def __init__(self, label:str, slider_range:tuple[int,int] , parent=None):
        super().__init__(parent)

        self.description_label = QLabel()
        self.description_label.setText(label)

        self.value_label = QLabel()
        self.value_label.setText(label)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(slider_range[0], slider_range[1])

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    def set_value(self, value):
        self.slider.setValue(value)

    def set_text(self, text):
        self.value_label.setText(text)

class ForceSensorMainWindow(QMainWindow):
    def __init__(self, shared_memory_client: ForceSensorSharedMemoryClient):
        # TODO make this look nice
        super().__init__()

        self.setWindowTitle("Force Reader")

        self.setMinimumHeight(400)

        self.shared_memory_client: ForceSensorSharedMemoryClient = shared_memory_client

        self.timer_ = QTimer()
        self.timer_.timeout.connect(self._timer_callback)
        self.timer_.start(1)

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self)

        self.force_slider = SliderLabelVertical("Force Norm", (-300,300), self)
        self.torque_slider = SliderLabelVertical("Torque Norm", (-300,300), self)

        self.plot_f = pg.plot(title="My Title")
        self.fx_queue = Queue(maxsize=100)
        self.plot_f.plot([])

        self.layout.addWidget(self.force_slider)
        self.layout.addWidget(self.torque_slider)
        self.layout.addWidget(self.plot_f)

        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)


    def _timer_callback(self):
        try:
            if self.shared_memory_client.is_open():
                wrench = self.shared_memory_client.get_wrench()

                f = np.array(wrench[0:3])
                f_norm = np.linalg.norm(f)
                if self.fx_queue.full():
                    self.fx_queue.get()
                self.fx_queue.put(f[0])
                self.plot_f.setData((np.asarray(self.fx_queue.queue), np.linspace(0,1,self.fx_queue.qsize())))
                self.force_slider.set_value(int(f_norm))
                self.force_slider.set_text('{:.2f}'.format(f_norm))

                t = np.array(wrench[3:5])
                t_norm = np.linalg.norm(t)
                self.torque_slider.set_value(int(t_norm))
                self.torque_slider.set_text('{:.2f}'.format(t_norm))

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
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

import qdarktheme
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
        # ---- make this look nice.
        # TODO make this look nicer
        super().__init__()

        self.setWindowTitle("MarinhoLab's Force Sensor Reader")

        self.setMinimumHeight(400)

        self.shared_memory_client: ForceSensorSharedMemoryClient = shared_memory_client

        self.timer_ = QTimer()
        self.timer_.timeout.connect(self._timer_callback)
        self.timer_.start(1)

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self)

        self.force_slider = SliderLabelVertical("Force Norm", (-300,300), self)
        self.torque_slider = SliderLabelVertical("Torque Norm", (-300,300), self)

        self.force_plot_layout = QVBoxLayout()
        self.plot_fx = pg.plot(title="f_x")
        self.plot_fy = pg.plot(title="f_y")
        self.plot_fz = pg.plot(title="f_z")
        self.fx_queue = Queue(maxsize=200)
        self.fx_lims = [0,0]
        self.fy_lims = [0,0]
        self.fz_lims = [0,0]
        self.fy_queue = Queue(maxsize=200)
        self.fz_queue = Queue(maxsize=200)
        self.data_fx = self.plot_fx.plot([])
        self.data_fy = self.plot_fy.plot([])
        self.data_fz = self.plot_fz.plot([])
        self.force_plot_layout.addWidget(self.plot_fx)
        self.force_plot_layout.addWidget(self.plot_fy)
        self.force_plot_layout.addWidget(self.plot_fz)

        self.torque_plot_layout = QVBoxLayout()
        self.plot_tx = pg.plot(title="\tau_x")
        self.plot_ty = pg.plot(title="\tau_y")
        self.plot_tz = pg.plot(title="\tau_z")
        self.tx_lims = [0,0]
        self.ty_lims = [0,0]
        self.tz_lims = [0,0]
        self.tx_queue = Queue(maxsize=200)
        self.ty_queue = Queue(maxsize=200)
        self.tz_queue = Queue(maxsize=200)
        self.data_tx = self.plot_tx.plot([])
        self.data_ty = self.plot_ty.plot([])
        self.data_tz = self.plot_tz.plot([])
        self.torque_plot_layout.addWidget(self.plot_tx)
        self.torque_plot_layout.addWidget(self.plot_ty)
        self.torque_plot_layout.addWidget(self.plot_tz)

        self.layout.addWidget(self.force_slider)
        self.layout.addWidget(self.torque_slider)
        self.layout.addLayout(self.force_plot_layout)
        self.layout.addLayout(self.torque_plot_layout)

        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)


    def _timer_callback(self):
        try:
            if self.shared_memory_client.is_open():
                wrench = self.shared_memory_client.get_wrench()

                f = np.array(wrench[0:3])
                t = np.array(wrench[3:6])
                f_norm = np.linalg.norm(f)

                if self.fx_queue.full():
                    self.fx_queue.get()
                self.fx_queue.put(f[0])
                current_data = np.asarray(self.fx_queue.queue)
                self.fx_lims[0] = min(self.fx_lims[0], np.min(current_data))
                self.fx_lims[1] = max(self.fx_lims[1], np.max(current_data))
                self.data_fx.setData(np.linspace(0, 1, self.fx_queue.qsize()), current_data)
                self.plot_fx.setYRange(self.fx_lims[0], self.fx_lims[1])
                self.plot_fx.setTitle("fx")

                if self.fy_queue.full():
                    self.fy_queue.get()
                self.fy_queue.put(f[1])
                current_data = np.asarray(self.fy_queue.queue)
                self.fy_lims[0] = min(self.fy_lims[0], np.min(current_data))
                self.fy_lims[1] = max(self.fy_lims[1], np.max(current_data))
                self.data_fy.setData(np.linspace(0, 1, self.fy_queue.qsize()), current_data)
                self.plot_fy.setYRange(self.fy_lims[0], self.fy_lims[1])
                self.plot_fy.setTitle("fy")

                if self.fz_queue.full():
                    self.fz_queue.get()
                self.fz_queue.put(f[2])
                current_data = np.asarray(self.fz_queue.queue)
                self.fz_lims[0] = min(self.fz_lims[0], np.min(current_data))
                self.fz_lims[1] = max(self.fz_lims[1], np.max(current_data))
                self.data_fz.setData(np.linspace(0, 1, self.fz_queue.qsize()), current_data)
                self.plot_fz.setYRange(self.fz_lims[0], self.fz_lims[1])
                self.plot_fz.setTitle("fz")

                if self.tx_queue.full():
                    self.tx_queue.get()
                self.tx_queue.put(t[0])
                current_data = np.asarray(self.tx_queue.queue)
                self.tx_lims[0] = min(self.tx_lims[0], np.min(current_data))
                self.tx_lims[1] = max(self.tx_lims[1], np.max(current_data))
                self.data_tx.setData(np.linspace(0, 1, self.tx_queue.qsize()), current_data)
                self.plot_tx.setYRange(self.tx_lims[0], self.tx_lims[1])
                self.plot_tx.setTitle("tx")

                if self.ty_queue.full():
                    self.ty_queue.get()
                self.ty_queue.put(t[1])
                current_data = np.asarray(self.ty_queue.queue)
                self.ty_lims[0] = min(self.ty_lims[0], np.min(current_data))
                self.ty_lims[1] = max(self.ty_lims[1], np.max(current_data))
                self.data_ty.setData(np.linspace(0, 1, self.ty_queue.qsize()), current_data)
                self.plot_ty.setYRange(self.ty_lims[0], self.ty_lims[1])
                self.plot_ty.setTitle("ty")

                if self.tz_queue.full():
                    self.tz_queue.get()
                self.tz_queue.put(t[2])
                current_data = np.asarray(self.tz_queue.queue)
                self.tz_lims[0] = min(self.tz_lims[0], np.min(current_data))
                self.tz_lims[1] = max(self.tz_lims[1], np.max(current_data))
                self.data_tz.setData(np.linspace(0, 1, self.tz_queue.qsize()), current_data)
                self.plot_tz.setYRange(self.tz_lims[0], self.tz_lims[1])
                self.plot_tz.setTitle("tz")

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
        qdarktheme.setup_theme()
        myapp.show()
        app.exec()
    except Exception as e:
        print("umirobot_main_window::run::Error::" + str(e))
    except KeyboardInterrupt:
        print("umirobot_main_window::run::Info::Interrupted by user.")

    shared_memory_client.send_shutdown_flag(True)
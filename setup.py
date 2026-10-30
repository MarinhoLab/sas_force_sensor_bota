# Copyright (c) 2012-2026 Murilo Marques Marinho
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

import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'sas_force_sensor_bota'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.json'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml')))
    ],
    install_requires=['setuptools', 'bota-driver'],
    zip_safe=True,
    maintainer='Murilo Marinho',
    maintainer_email='murilo.marinho@manchester.ac.uk',
    description='Bota Systems force torque sensor package compliant with the SmartArmStack sas framework',
    license='LGPL-3.0-or-later',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "sas_force_sensor_bota_node = sas_force_sensor_bota.main:main",
            "sas_force_sensor_client_example_node = sas_force_sensor_bota.sas_force_sensor_client_example:main",
        ],
    },
)

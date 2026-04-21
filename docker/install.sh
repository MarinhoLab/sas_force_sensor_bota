#!/bin/bash
set -e
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y libxcb-cursor-dev
python3 -m pip install bota_driver PyQt6 pyqtgraph --break-system-packages
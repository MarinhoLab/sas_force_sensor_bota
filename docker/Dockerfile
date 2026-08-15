FROM murilomarinho/sas:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN sudo apt-get update && sudo apt-get upgrade -y

COPY install.sh /root/sas_force_sensor_bota/
RUN cd /root/sas_force_sensor_bota \
    && chmod +x install.sh \
    && . install.sh

RUN python3 -m pip install --upgrade dqrobotics --break-system-packages
RUN sudo sudo apt-get remove -y ros-jazzy-sas-force-sensor-bota
RUN mkdir -p /root/sas_force_sensor_bota_devel/src/
COPY . /root/sas_force_sensor_bota_devel/src/sas_force_sensor_bota

#!/bin/sh

echo "Starting the Loraship program"
mkdir /mnt/mmcblk0p1/ifremer_data
/usr/bin/micropython /root/RAK7289_standalone_server/mqtt_sub.py &> /dev/null &
echo "Saving PID of subprocess in /root/RAK7289_standalone_server/mqtt_sub.pid"
echo $! > /root/RAK7289_standalone_server/mqtt_sub.pid
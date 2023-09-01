#!/bin/sh

echo "Starting the Loraship program"
mkdir /mnt/mmcblk0p1/ifremer_data
/usr/bin/micropython /root/ifremer/python/mqtt_sub.py &> /dev/null &
echo "Saving PID of subprocess in /root/ifremer/python/mqtt_sub.pid"
echo $! > /root/ifremer/python/mqtt_sub.pid
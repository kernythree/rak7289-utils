#!/bin/sh

echo "Starting the Loraship program"
# without log file
/usr/bin/micropython /root/ifremer/python/mqtt_sub.py &
# with log file
# /usr/bin/micropython /root/ifremer/python/mqtt_sub.py > /mnt/mmcblk0p1/ifremer_data/mqtt_sub.log &

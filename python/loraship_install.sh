#!/bin/sh

echo "Installing loraship program as service"
cp loraship_mqtt_service /etc/init.d
chmod +x /etc/init.d/loraship_mqtt_service
/etc/init.d/loraship_mqtt_service enable
/etc/init.d/loraship_mqtt_service reload
echo "Done"

echo "Adding mail_send.py in crontab"
echo "0 */2 * * * cd /root/ifremer/python/ ; micropython mail_send.py" >> /etc/crontabs/root
/etc/init.d/cron restart
echo "Done"

echo "Installation has finish. Best if host is reboot now."
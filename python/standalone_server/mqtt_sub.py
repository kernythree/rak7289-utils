##################################
# Loraship Project (Ifremer 2023)
##################################

import time
import os
from umqtt.simple import MQTTClient

SERVER = "127.0.0.1"
clientid = 'localclient'
user = ""
password = ""
topic = "application/#"
msg = b'{"data":"hello"}'

file_path = '/mnt/mmcblk0p1/ifremer_data/'
dfile_name = 'last_lora_data.txt'
sfile_name = 'mqtt_client_status.txt'

def sub(topic, msg):
    print('received message %s on topic %s' % (msg, topic))
    print('save to file')
    try:
        with open(file_path + dfile_name, "a") as f:
            f.write(msg+'\n')
    except:
        print('out file can not be reached (busy?), msg will not be saved')

def main(server=SERVER):
    client = MQTTClient(clientid, server, 1883, user, password)
    client.set_callback(sub)
    client.connect()
    print('Connected to MQTT Broker "%s"' % (server))
    with open(file_path + sfile_name, "a") as f:
        d = time.gmtime()
        curdate = str(d[0])+'-'+str(d[1])+'-'+str(d[2])+'_'+str(d[3])+'h'+str(d[4])+'m'+str(d[5])+'s'
        f.write('('+curdate+') '+'mqtt client restarted on topic ' + topic + '\n')


    client.subscribe(topic)
    while True:
        if True:
            client.wait_msg()
        else:
            client.check_msg()
            time.sleep(1)

if __name__ == "__main__":
    main()

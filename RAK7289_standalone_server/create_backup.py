##################################
# Loraship Project (Ifremer 2023)
##################################

import os
import time

# file in flash where lora data are saved by script mqtt_sub.py
infile_path = '/mnt/mmcblk0p1/ifremer_data/'
infile_name = 'last_lora_data.txt'
infile_name_mqtt = 'mqtt_client_status.txt'

#def boundary():
#    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOUPQRSTUWVXYZ') for i in range(15))


def get_gateway_eui():
    os.system("cat  /etc/config/einfo | grep gw_eui | sed 's/.* //' > tmp")
    gweui = open('tmp', 'r').read()
    gweui = gweui[1:-2]
    os.remove('tmp')
    return gweui

def get_gateway_info_short():
    print('Reading gateway info')
    os.system('echo ----- Gateway EUI ----- > tmp')
    os.system("cat  /etc/config/einfo | grep gw_eui | sed 's/.* //' >> tmp")
    os.system('echo ----- System and OS version ----- >> tmp')
    os.system('uname -a >> tmp')
    os.system('cat  /etc/openwrt_version >> tmp')
    os.system('echo ----- Current date and Uptime ----- >> tmp')
    os.system('date >> tmp')
    os.system('uptime >> tmp')
    os.system('echo ----- Memory Usage ----- >> tmp')
    os.system('df -h >> tmp')
    gwinfo = open('tmp', 'r').read()
    os.remove('tmp')
    return gwinfo

def get_gateway_info():
    print('Reading gateway info')
    os.system('echo ----- Gateway EUI ----- > tmp')
    os.system("cat  /etc/config/einfo | grep gw_eui | sed 's/.* //' >> tmp")
    os.system('echo ----- System and OS version ----- >> tmp')
    os.system('uname -a >> tmp')
    os.system('cat  /etc/openwrt_version >> tmp')
    os.system('echo ----- Current date and Uptime ----- >> tmp')
    os.system('date >> tmp')
    os.system('uptime >> tmp')
    os.system('echo ----- Memory Usage ----- >> tmp')
    os.system('df -h >> tmp')
    os.system('echo ----- General Config ----- >> tmp')
    os.system('cat  /etc/config/einfo >> tmp')
    os.system('echo ----- Lora Server Config ----- >> tmp')
    os.system('cat  /etc/config/lorasrv >> tmp')
    os.system('echo ----- Network Config ----- >> tmp')
    os.system('cat  /etc/config/network >> tmp')
    os.system('echo ----- MQTT client last activity ----- >> tmp')
    os.system('tail -n 5 '+infile_path+infile_name_mqtt+' >> tmp')
    gwinfo = open('tmp', 'r').read()
    os.remove('tmp')
    return gwinfo

def copy_save_lora_data_file():
    res = False
    outfile = {'name':'undef','content':None}
    gweui = get_gateway_eui()
    d = time.gmtime()
    curdate = str(d[0])+'-'+str(d[1])+'-'+str(d[2])+'_'+str(d[3])+'h'+str(d[4])+'m'+str(d[5])+'s'
    outfile['name'] = 'lora_data_gw_'+gweui+'_'+curdate+'.txt'
    print('copying current data file ('+infile_name+') to stored version ('+outfile['name']+')')
    try:
        os.system('cp ' + infile_path + infile_name + ' ' + infile_path + outfile['name'])
        os.system('rm ' + infile_path + infile_name)
        res = True
    except OSError:
        print('Error whth data file')
        os.system('echo "no content avalaible, gateway received no LoRa message" > ' + infile_path + outfile['name'])
        res = False
    return res

def main():
    # Create backup
    result = copy_save_lora_data_file()

if __name__ == "__main__":
    main()

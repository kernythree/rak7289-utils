##################################
# Loraship Project (Ifremer 2023)
##################################

# Micropython lib to send emails: https://github.com/shawwwn/uMail
# solution to send attachements : https://github.com/shawwwn/uMail/issues/2
import umail
import ubinascii
import urandom as random
import os
import time

# Host details
host = '108.177.15.108' # 'smtp.gmail.com'
port = '465' # to be used with TLS/SSL, use port 587 otherwise

# Sender details
sender_email = 'loraship.ifremer@gmail.com'
sender_name = 'loraship.ifremer' #sender name
sender_app_password = 'wklycdvibzgsxqoo' # application key to be generated in gmail

# file in flash where lora data are saved by script mqtt_sub.py
infile_path = '/mnt/mmcblk0p1/ifremer_data/'
infile_name = 'last_lora_data.txt'
infile_name_mqtt = 'mqtt_client_status.txt'

#def boundary():
#    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOUPQRSTUWVXYZ') for i in range(15))

def send_mail(email, attachment = None):
    # log into smtp server
    print('logging to SMTP host ' + host + ' as ' + sender_email)
    smtp = umail.SMTP(host, port, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    print('done')
    # build email with attachement
    smtp.to(email['to'])
    smtp.write("From: {0} <{1}>\n".format(sender_name,sender_email))
    smtp.write("To: {0} <{0}>\n".format(email['to']))
    smtp.write("Subject: {0}\n".format(email['subject']))
    if attachment:
        text_id = '5350123048127315795' #boundary()
        attachment_id = '12345678900987654321' #boundary()
        smtp.write("MIME-Version: 1.0\n")
        smtp.write('Content-Type: multipart/mixed;\n boundary="------------{0}"\n'.format(attachment_id))
        smtp.write('--------------{0}\nContent-Type: multipart/alternative;\n boundary="------------{1}"\n\n'.format(attachment_id, text_id))
        smtp.write('--------------{0}\nContent-Type: text/plain; charset=utf-8; format=flowed\nContent-Transfer-Encoding: 7bit\n\n{1}\n\n--------------{0}--\n\n'.format(text_id, email['text']))
        smtp.write('--------------{0}\nContent-Type: image/jpeg;\n name="{1}"\nContent-Transfer-Encoding: base64\nContent-Disposition: attachment;\n  filename="{1}"\n\n'.format(attachment_id, attachment['name']))
        b64 = ubinascii.b2a_base64(attachment['bytes'])
        smtp.write(b64)
        smtp.write('--------------{0}--'.format(attachment_id))
    else:
        smtp.write(email['text'])
    print('sending email')    
    smtp.send()
    smtp.quit()
    print('done')

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
    outfile = {'name':'undef','content':None}
    gweui = get_gateway_eui()
    d = time.gmtime()
    curdate = str(d[0])+'-'+str(d[1])+'-'+str(d[2])+'_'+str(d[3])+'h'+str(d[4])+'m'+str(d[5])+'s'
    outfile['name'] = 'lora_data_gw_'+gweui+'_'+curdate+'.txt'
    print('copying current data file ('+infile_name+') to stored version ('+outfile['name']+')')
    try:
        os.system('cp ' + infile_path + infile_name + ' ' + infile_path + outfile['name'])
        with open(infile_path + outfile['name'], "r") as f:
            outfile['content'] = f.read()
            print(outfile['content'])
        os.system('rm ' + infile_path + infile_name)
    except OSError:
        print('Error whth data file')
        outfile['content'] = 'no content avalaible, file may not exist on the gateway ...'
    return outfile

def main():
    ### Send email with gateway data
    gweui = get_gateway_eui()
    # Email details 
    recipient_email ='loraship.ifremer@gmail.com'
    email_subject ='Loraship - Gateway Daily Data ' + '('+gweui+')'
    # Email text
    email_text = get_gateway_info_short()
    # Email attachement
    outfile = copy_save_lora_data_file()
    # call send func
    send_mail({'to': recipient_email, 'subject': email_subject, 'text': email_text},
              {'bytes' : outfile['content'], 'name' : outfile['name']})
    ### Send email with gateway data
    gweui = get_gateway_eui()
    # Email details 
    recipient_email ='loraship.ifremer@gmail.com'
    email_subject ='Loraship - Gateway Daily Status ' + '('+gweui+')'
    # Email text
    email_text = get_gateway_info()
    # Email attachement
    d = time.gmtime()
    curdate = str(d[0])+'-'+str(d[1])+'-'+str(d[2])+'_'+str(d[3])+'h'+str(d[4])+'m'+str(d[5])+'s'
    outfile['name'] = 'status_gw_'+gweui+'_'+curdate+'.txt'
    os.system('logread | tail -n 2000 > tmp')
    outfile['content'] = open('tmp', 'r').read()
    os.remove('tmp')
    # call send func
    send_mail({'to': recipient_email, 'subject': email_subject, 'text': email_text},
              {'bytes' : outfile['content'], 'name' : outfile['name']})

if __name__ == "__main__":
    main()

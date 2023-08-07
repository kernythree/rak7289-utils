# Complete project details: https://RandomNerdTutorials.com/micropython-send-emails-esp32-esp826/
# Micropython lib to send emails: https://github.com/shawwwn/uMail
import umail
#import network

host = '108.177.15.108' # 'smtp.gmail.com'
port = '465' # to be used with TLS, use 587 otherwise

# Email details
sender_email = 'loraship.ifremer@gmail.com'
sender_name = 'loraship.ifremer' #sender name
sender_app_password = 'wklycdvibzgsxqoo'
recipient_email ='loraship.ifremer@gmail.com'
email_subject ='Test Email'


# Send the email
smtp = umail.SMTP(host, port, ssl=True) # Gmail's SSL port
print('try to log in')
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write("Hello from ESP32")
smtp.send()
smtp.quit()

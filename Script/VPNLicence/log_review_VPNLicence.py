import os
import csv
import sys
import fileinput
from datetime import date, timedelta, datetime
import smtplib
import platform
from email.message import EmailMessage
from time import process_time
import re
import subprocess

startTime = process_time()

path = os.getcwd()

todate = date.today()
#todate = datetime(2022, 9, 22)

server = '10.1.0.73'
hostName = platform.uname()[1]
mailStatus = "Log Review(VPNLicence) - "
mailBody = ""

fileName = (todate - timedelta(days = 7)).strftime("%Y%m%d") + " To " + (todate - timedelta(days = 1)).strftime("%Y%m%d")

message = EmailMessage()
message['From'] = 'team5@housingauthority.gov.hk'
#message['To'] = 'kingshun.fung@housingauthority.gov.hk'
message['To'] = 'kingshun.fung@housingauthority.gov.hk, tonywp.ho@housingauthority.gov.hk, pingfuk.lam@housingauthority.gov.hk'

path = r"E:/"
#path = 'C:/Users/KingShunFung/Desktop/log_data'

keywords = ["login", "logout", "major", "error"]
files = []
dateList = []
#ipList = ["172.29.1.57", "172.29.1.58"]
ipList = ["172.31.1.120"]

p = subprocess.Popen(["powershell",".\check_syslog_status.ps1"], stdout=subprocess.PIPE)
p_out, p_err = p.communicate()

syslogServerStatus=False
print(p_out)
if "Running" in str(p_out):
    syslogServerStatus=True
print(syslogServerStatus)

for i in range(1, 8):
    dateList.append((todate - timedelta(days = i)).strftime("%Y%m%d"))

print(dateList)

for r, d, f in os.walk(path):
    for file in f:
        if '.log' in file:
            for ip in ipList:
                for date in dateList:
                    if ip in file and date in file:
                        files.append(os.path.join(r, file))
                        print(os.path.join(r, file))

print()

for f in files:
    print(f)
    logFile = f
    #Lines = logFile.readlines()
    for line in fileinput.input(files=logFile, encoding='unicode_escape'):
        #print(line)
        lower_line = line.lower()
        if 'vpnadmin' in lower_line:
            for keyword in keywords:
                if keyword in lower_line:
                    mailBody = mailBody + line

attachment = mailBody.encode('utf-8')

endTime = process_time()

minus = int(int(endTime - startTime)/60)
seconds = (int(endTime - startTime))%60

content = ''
#content = content + "\n" + "\n" + "Total Process Time: " + str(minus) + "min" + str(seconds) + "s\n"
content = content + "Checked Date: From " + fileName
content = content + "\nChecked IP: " + str(ipList)

if syslogServerStatus:
    content = content + "\nThe Status of Syslog server: Running"
else:
    content = content + "\nThe Status of Syslog server: No Response"

message.set_content(content)
message.add_attachment(attachment, maintype='application', subtype='log', filename=fileName + '.log')

if syslogServerStatus:
    message['Subject'] = mailStatus + 'Checked from ' + hostName + " & Status of Syslog Server: Running"
else:
    message['Subject'] = mailStatus + 'Checked from ' + hostName + " & Status of Syslog Server: No Response"
             
smtp = smtplib.SMTP(server, 25)
smtp.send_message(message)

smtp.quit()                

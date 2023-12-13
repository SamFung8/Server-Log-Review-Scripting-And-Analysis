import os
import csv
import sys
import fileinput
from datetime import date, timedelta, datetime
import smtplib
import platform
from email.message import EmailMessage
from time import process_time

startTime = process_time()

server = '172.29.10.127'
hostName = platform.uname()[1]
mailStatus = "Log Review(DNS) - "
mailBody = ""

message = EmailMessage()
message['From'] = ''
message['To'] = ''
#message['To'] = ''

path = 'D:\syslog'


keywords = ["Login_Allowed", "Login_Denied", "Logout", "Password_Reset"]
files = []
dateList = []
ipList = ["172.29.1.57", "172.29.1.58"]
#ipList = ["10.24.2.124", "10.24.2.123"]


todate = date.today()
#todate = datetime(2022, 9, 22)
for i in range(1, 8):
    dateList.append((todate - timedelta(days = i)).strftime("%Y%m%d"))

print(dateList)

for r, d, f in os.walk(path):
    for file in f:
        for ip in ipList:
            for date in dateList:
                if '.log' in file and ip in file and date in file:
                    files.append(os.path.join(r, file))
                    print(os.path.join(r, file))

print()

for f in files:
    print(f)
    logFile = f
    #Lines = logFile.readlines()
    for line in fileinput.input([logFile]):
        #print(line)
        for keyword in keywords:
            if keyword in line:
                print(line)
                mailBody = mailBody + line

attachment = mailBody.encode('utf-8')

endTime = process_time()

minus = int(int(endTime - startTime)/60)
seconds = (int(endTime - startTime))%60

mailBody = mailBody + "\n" + "\n" + "Total Process Time: " + str(minus) + "min" + str(seconds) + "s\n"
mailBody = mailBody + "Checked Date: From " + (todate - timedelta(days = 7)).strftime("%Y%m%d") + " To " + (todate - timedelta(days = 1)).strftime("%Y%m%d")
mailBody = mailBody + "\nChecked IP: " + str(ipList)

message.set_content(mailBody)
message.add_attachment(attachment, maintype='application', subtype='log', filename=(todate - timedelta(days = 7)).strftime("%Y%m%d") + " To " + (todate - timedelta(days = 1)).strftime("%Y%m%d") + '.log')                
message['Subject'] = mailStatus + 'Checked from ' + hostName
smtp = smtplib.SMTP(server, 25)
smtp.send_message(message)
smtp.quit()                

#!/usr/bin/python3
#-*- coding:UTF-8 -*-

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import _sqlite3
import time

cx = _sqlite3.connect("tickets.db")
sender = '*********@126.com'
username = '*********@126.com'
password = '*************' #please use the SMTP code
email_server = 'smtp.126.com'
smtp_port = 465

class dbInfo:
    name = ''
    enname = ''
    cell = ''
    email = ''
    club = ''
    def __init__(self, TNAME, TENNAME, TCELL, TEMAIL, TCLUB):
        self.name = TNAME
        self.enname = TENNAME
        self.cell = TCELL
        self.email = TEMAIL
        self.club = TCLUB

def getInfo():
    receiverInfos = []
    sql = "select TNAME, TENNAME, TCELL, TEMAIL, TCLUB from TB_TICKETINFO"
    cursor = cx.execute(sql)

    for row in cursor:
        rInfo = dbInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
        receiverInfos.append(rInfo)

    return receiverInfos

#send email using html
def sendEmail(receiver,receiverInfo,number):
    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = sender
    msgRoot['To'] = Header(receiver, 'utf-8')
    subject = '*********'
    msgRoot['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #英文的内容
    mail_msg = """
    <!DOCTYPE html>
    <html>
    <p><img src="cid:image1"></p>
    <p><b>Dear %s</b></p>
    <p>Please check your information. If something is wrong or missed here, please feel free to let us know.</p>
    <table border="1">
    <tr>
        <td>Ticket No.</td>
        <td>%d</td>
    </tr>
    <tr>
        <td>Chinese Name</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>English Name</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Club</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Mobile</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Email</td>
        <td>%s</td>
    </tr>
    </table>
    <p><img src="cid:image2"></p>
    </html>
    """ % (receiverInfo.enname, number, receiverInfo.name,receiverInfo.enname, receiverInfo.club, receiverInfo.cell, receiverInfo.email)

    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    #image 1
    fp = open('ti.jpg', 'rb')
    msgImage_Title = MIMEImage(fp.read())
    fp.close()
    msgImage_Title.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage_Title)

    #image2
    fp = open('wx.jpg', 'rb')
    msgImage_wx = MIMEImage(fp.read())
    fp.close()
    msgImage_wx.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage_wx)

    try:
        smtp = smtplib.SMTP_SSL(email_server, smtp_port, 'localhost')
        smtp.set_debuglevel(1)
        smtp.helo(email_server)
        smtp.ehlo(email_server)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msgRoot.as_string())
        smtp.quit()
        return 0
    except smtplib.SMTPException:
        print("Error: Failed")
        return -1


#main part
receiverFailList = []
receiverList = []
receiverList = getInfo()
count = 1

for i_receiver in receiverList:
    print(i_receiver.name)
    status = sendEmail(i_receiver.email, i_receiver, count)
    if status == -1:
        receiverFailList.append(i_receiver)
    count = count + 1
    #time.sleep(5)

if len(receiverFailList) > 0:
    for i_fail in receiverFailList:
        print(i_fail.cell)

cx.close()

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
sender = '************@126.com'
username = '**************@126.com'
password = '****************'
email_server = 'smtp.126.com'
smtp_port = 465

class dbInfo:
    name = ''
    enname = ''
    cell = ''
    email = ''
    club = ''
    status = 0 #send success:0, send success: 1
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
    #cx.commit()

    for row in cursor:
        rInfo = dbInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
        receiverInfos.append(rInfo)

    return receiverInfos

#send email using html
def sendEmail(receiver,receiverInfo,number):
    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = sender
    msgRoot['To'] = Header(receiver, 'utf-8')
    subject = '【TMC】【2017 NJ Conference】2017南京秋季峰会票务确认函'
    msgRoot['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #英文的内容
    mail_msg = """
    <!DOCTYPE html>
    <html>
    <p><img src="cid:image1"></p>
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

    #中文的内容
    mail_msg_cn = """
       <!DOCTYPE html>
       <html>
       <p><b>尊敬的 %s</b></p>
       <p>以下是您的信息，如果以下信息有错漏的内容，请回复我们补齐。</p>
       <table border="1">
       <tr>
           <td>票号</td>
           <td>%d</td>
       </tr>
       <tr>
           <td>中文名</td>
           <td>%s</td>
       </tr>
       <tr>
           <td>英文名</td>
           <td>%s</td>
       </tr>
       <tr>
           <td>俱乐部</td>
           <td>%s</td>
       </tr>
       <tr>
           <td>联系电话</td>
           <td>%s</td>
       </tr>
       <tr>
           <td>邮箱</td>
           <td>%s</td>
       </tr>
       </table>
       <p><img src="cid:image3"></p>
       </html>
       """ % (receiverInfo.enname, number, receiverInfo.name, receiverInfo.enname, receiverInfo.club, receiverInfo.cell,
              receiverInfo.email)

    msgAlternative.attach(MIMEText(mail_msg_cn, 'html', 'utf-8'))

    #image 1
    # 指定图片为当前目录
    fp = open('ti.jpg', 'rb')
    msgImage_Title = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage_Title.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage_Title)

    #image2
    # 指定图片为当前目录
    fp = open('wx.jpg', 'rb')
    msgImage_wx = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage_wx.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage_wx)

    #image3
    # 指定图片为当前目录
    fp = open('wx.jpg', 'rb')
    msgImage_wx_cn = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage_wx_cn.add_header('Content-ID', '<image3>')
    msgRoot.attach(msgImage_wx_cn)

    smtp = smtplib.SMTP(email_server, smtp_port)
    smtp.starttls()
    #smtp.set_debuglevel(1)
    #smtp = smtplib.SMTP_SSL('smtp.126.com', 465)
    #smtp.connect(email_server)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
    return 0


#main part
receiverFailList = []
receiverList = []
receiverList = getInfo()
count = 1

for i_receiver in receiverList:
    print(i_receiver.name)
    status = sendEmail(receiver, i_receiver, count)
    if status == -1:
        receiverFailList.append(i_receiver)
    count = count + 1
    time.sleep(5)

if len(receiverFailList) > 0:
    for i_fail in receiverFailList:
        print(i_fail.cell)

cx.close()
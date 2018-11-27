# import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# 发件人邮箱
_fromMail = "2459238021@qq.com"


def buildMailWithAttribute(subject, toMail):
    '''
    创建邮件并配置属性
    :param subject: 邮件主题
    :param toMail:  收件人邮箱列表
    :return: 邮件对象
    '''
    # 创建对象邮件
    mail = MIMEMultipart()
    # 配置邮件属性
    mail['Subject'] = subject
    mail['From'] = _fromMail
    mail['To'] = ','.join(toMail)
    return mail


def addTextMailBody(mail, textBody):
    '''
    添加邮件正文到邮件对象（正文为纯文本格式）
    :param mail: 需添加正文的邮件
    :param textBody: 正文
    :return: 邮件对象
    '''
    textMsg = MIMEText(textBody, _charset='utf-8')
    mail.attach(textMsg)


def addHtmlMailBody(mail, htmlBody):
    '''
    添加邮件正文到邮件对象（正文为Html格式）
    :param mail: 需添加正文的邮件
    :param htmlBody: 正文
    :return: 邮件对象
    '''
    htmlBody = MIMEText(htmlBody, _subtype='html', _charset='utf-8')
    mail.attach(htmlBody)


def addMailAttachment(mail, files):
    '''
    添加邮件附件
    :param mail:  需添加附件的邮件
    :param files: 文件列表
    :return: 邮件对象
    '''
    for fileUri in files:
        with open(fileUri, 'rb') as file:
            mailAttachment = MIMEBase("application", "octet-stream")
            mailAttachment.set_payload(file.read())
            encoders.encode_base64(mailAttachment)
            mailAttachment.add_header("Content-Disposition", "attachment",
                                  filename=('gbk', '', fileUri.split('\\')[-1]))    # gbk编码防止附件名乱码
            mail.attach(mailAttachment)
    return mail


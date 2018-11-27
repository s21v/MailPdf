import smtplib
import Mail
import FileDealers


# SMTP服务器地址　端口号
_smtpServer = "smtp.qq.com"
_smtpPort = 465
# 邮件发送方信息
_fromMail = "2459238021@qq.com"
_password = "hxlezkqqmnjndjah"   # 授权码
# 邮件接收方信息
to_mail = ["925623007@qq.com"]


def sendMail(subject, toMail, msg, attachmentFiles, isHtml):
    try:
        # 配置邮件服务器信息
        smtp = smtplib.SMTP_SSL(_smtpServer, _smtpPort)
        # 传入相应的账号密码
        smtp.login(_fromMail, _password)
        mail = Mail.buildMailWithAttribute(subject, toMail)
        if isHtml is False:
            Mail.addTextMailBody(mail, msg)
        else:
            Mail.addHtmlMailBody(mail, msg)
        if len(attachmentFiles) != 0:
            Mail.addMailAttachment(mail, attachmentFiles)
        # 发送邮件
        smtp.sendmail(_fromMail, toMail, mail.as_string())
    except smtplib.SMTPException as e:
        print(e.message)
    finally:
        smtp.quit()
        

def main():
    year = int(input("请输入年份："))
    month = int(input("请输入月份（1-12）："))
    # 复制文件
    FileDealers.copyFile(year, month)
    # 压缩文件
    attachmentFileUri = FileDealers.zipDir(year, month)
    if attachmentFileUri is not None:
        subject = '山东周刊{0:4d}年{1:d}月pdf文件汇总'.format(year, month)
        textMsg = '请下载附件，解压缩后查看。'
        attachmentFileUris = list()
        attachmentFileUris.append(attachmentFileUri)
        # 发送邮件
        print("邮件发送中，请耐心等待。。。")
        sendMail(subject, to_mail, textMsg, attachmentFileUris, isHtml=False)


if __name__ == '__main__':
    main()
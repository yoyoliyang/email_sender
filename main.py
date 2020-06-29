import os
import sys
import smtplib
from email.message import EmailMessage

help_info = '需要输入参数 -h 查看帮助'


def check_argv():
    if len(sys.argv) == 1:
        return None
    if len(sys.argv) >= 1:
        if ('-s' and '-c' and '-t' and '-smtp' in sys.argv):
            if (sys.argv.count('-s') and sys.argv.count('-c') and sys.argv.count('-t') and sys.argv.count('-smtp') == 1):
                _s_index = sys.argv.index('-s')
                subject = sys.argv[_s_index+1]
                _c_index = sys.argv.index('-c')
                content = sys.argv[_c_index+1]
                _t_index = sys.argv.index('-t')
                receiver = sys.argv[_t_index+1]
                _smtp_index = sys.argv.index('-smtp')
                smtp = sys.argv[_smtp_index+1]
                try:
                    if len(smtp.split(':')) == 2:
                        if isinstance(int(smtp.split(':')[1]), int):
                            pass
                    else:
                        return None
                except IndexError or ValueError:
                    return None
                return subject, content, receiver, smtp
        if '-h' in sys.argv:
            print("""
用法：确保shell中已经配置好了EMAIL_USERNAME和EMAIL_PASSWORD的环境变量。
-s 标题
-c 内容
-t 收件人（多个收件人使用逗号分隔）
-smtp smtp地址及端口
示例：email_sender.py -smtp smtp.163.com:465 -s '邮件标题' -c '邮件正文' -t oceanlee@qq.com,leeocean@qq.com""")
        else:
            print(help_info)
            return None


def sender(*argvs):
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    if (EMAIL_ADDRESS and EMAIL_PASSWORD is not None):
        argvs = argvs[0]
        msg = EmailMessage()
        msg['Subject'] = argvs[0]
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = argvs[2].split(',')
        msg.set_content(argvs[1])
        with smtplib.SMTP_SSL(argvs[3].split(':')[0], argvs[3].split(':')[1]) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)
            print('发送完毕')
    else:
        print(help_info)


input = check_argv()
if input is not None:
    print(input)
    sender(input)
else:
    print(help_info)

import os
import subprocess
import ssl
from sleekxmpp import ClientXMPP

class MyXMPPBot(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.authorized_users = set()  # 已授权用户集合

        # 从 user.txt 文件读取已授权用户
        if os.path.exists("user.txt"):
            with open("user.txt", "r") as user_file:
                self.authorized_users = set(user_file.read().splitlines())

        # 注册事件处理程序
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            message = msg['body']
            response = ""

            if msg['from'].bare not in self.authorized_users:
                # 未授权用户需要发送 "hello3344521" 以获取授权
                if message == "hello3344521":
                    self.authorized_users.add(msg['from'].bare)
                    # 更新 user.txt 文件以包含已授权用户
                    with open("user.txt", "a") as user_file:
                        user_file.write(msg['from'].bare + "\n")
                    response = "已授权"
                else:
                    response = "未授权"
            else:
                if message.startswith("bash "):
                    command = message[5:]
                    try:
                        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                        response = result
                    except subprocess.CalledProcessError as e:
                        response = "错误: " + e.output
                else:
                    response = "呵呵"

            msg.reply(response).send()

if __name__ == '__main__':
    xmpp = MyXMPPBot('botgz@yangks.xyz', 'botgz.')

    # 禁用证书验证
    xmpp.ssl_version = ssl.PROTOCOL_TLS
    xmpp.cert_policy = ssl.CERT_NONE

    if xmpp.connect(address=('yangks.xyz', 5222)):
        xmpp.process(block=True)
    else:
        print("Unable to connect.")

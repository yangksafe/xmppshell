import requests
import time
import sleekxmpp

# 配置XMPP连接
username = 'bot-001@xmpp.jp'
password = 'bot001'
to_jid = 'coco@yangks.xyz'

class MyBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def check_stock(self, urls_to_check):
        while True:
            for url in urls_to_check:
                response = requests.get(url)
                if "Out of Stock" not in response.text:
                    self.send_message(mto=to_jid, mbody=f"链接 {url} 有库存了！")
            
            # 每隔十分钟检查一次
            time.sleep(600)  # 10分钟

if __name__ == '__main__':
    bot = MyBot(username, password)
    bot.connect()
    bot.process(forever=False)

    # 定义要检测的链接列表
    urls_to_check = [
        "https://my.frantech.ca/cart.php?a=add&pid=1423",
        "https://my.frantech.ca/cart.php?a=add&pid=1411",
        "https://my.frantech.ca/cart.php?a=add&pid=1413",
        "https://my.frantech.ca/cart.php?a=add&pid=1501",
    ]

    bot.check_stock(urls_to_check)


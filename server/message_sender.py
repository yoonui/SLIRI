import requests
import time

myToken = "xoxb-3451298675446-3443353129815-IPfyh7jGKWTRoJXg0HZGDLT2"

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                            headers={"Authorization": "Bearer " + token},
                            data={"channel": channel, "text": text}
                            )
    print(response)

def notice1():
    for i in range(5):
        post_message(myToken, "#project", "초인종이 울렸습니다!")

        time.sleep(5)

def notice2():
    for i in range(15):
        post_message(myToken, "#project", "화재경보가 울렸습니다!")

        time.sleep(3)


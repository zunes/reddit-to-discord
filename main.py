import os
import praw
import requests
import bottle
from threading import Thread

webhook=""

PORT = int(os.getenv('SERVER_PORT'))
           
@bottle.route('/')
def index():
    return "Hello World!"

def startWebServer():
  print("bottle starting")
  bottle.run(host='0.0.0.0', port=PORT)
  print("bottle running on "+PORT)
   

def startBot():
    reddit = praw.Reddit(client_id="MW3mGosBGbaogGJSVsKW-g",client_secret="4LGRxofyzYyamRz16kghjDbMNZKB0g",user_agent="reddit zunes bot",)
    class DemoRedditor:
        def __init__(self, name, icon_img):
            self.name = name
            self.icon_img = icon_img
    
    def SendMessage(redditor, title, url, body):
        print(redditor.name)
        print(redditor.icon_img)
        print(title)
        print(url)
        print(body)
        x = requests.post(webhook, json = { "embeds": [{ "color": 0xd6006c, "author": { "name": "u/" + redditor.name, "icon_url": redditor.icon_img if redditor.icon_img else "https://www.reddit.com/icon.png", "url": "https://reddit.com/u/" + redditor.name },  "title": title, "url": "https://reddit.com" + url, "description": body[0 : 4096] }] })
        print(x)

    SendMessage(DemoRedditor("zunesbot", "https://zunes.me/logo.png"), "now listening for reddit posts", "/r/zune", "is online")
    print("Ready!")

    try:
        for submission in reddit.subreddit('zune').stream.submissions(skip_existing=True):
            SendMessage(submission.author, submission.title, submission.permalink, submission.selftext)
            print("sent post to discord")
    except:
        print("An exception occurred")
    
    
    
    
if __name__ == "__main__":
    botThread = Thread(target=startBot)
    botThread.daemon = True
    botThread.start()

    webThread = Thread(target=startWebServer)
    webThread.start()

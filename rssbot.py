import feedparser
import time
import hashlib
from datetime import datetime, timedelta
import yhchat
import re
from bs4 import BeautifulSoup 

FEED_URL = "https://www.landiannews.com/feed"
PUSH_TOKEN = "328645231"  # Bot token
PUSH_GROUP = "group"  # 群组ID
INTERVAL = 60  # 检查间隔，单位：秒
MAX_IMAGE_HEIGHT = 160 # 图片最大高度，单位：像素

last_entry_guid = None


def check_rss_updates():
    global last_entry_guid

    try:
        feed = feedparser.parse(FEED_URL)
    except Exception as e:
        print(f"获取 RSS 订阅失败: {e}")
        return

    if not feed.entries:
        print("RSS 订阅中没有条目。")
        return

    latest_entry = feed.entries[0]

    if not last_entry_guid or latest_entry.guid != last_entry_guid:

        title = latest_entry.title
        link = latest_entry.link
        published = latest_entry.published_parsed
        published_datetime = datetime(*published[:6])
        published_formatted = published_datetime.strftime("%Y-%m-%d %H:%M:%S")

        content = ""
        if hasattr(latest_entry, 'content'): 
            content = latest_entry.content[0].value
        elif hasattr(latest_entry, 'summary'):
            content = latest_entry.summary

        content = re.sub(r"width=\"[^\"]*\"", "", content)
        content = re.sub(r"height=\"[^\"]*\"", "", content)
        content = re.sub(r"style=\"[^\"]*\"", "", content)

        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = 400

        soup = BeautifulSoup(content, "html.parser")

        for img in soup.find_all("img"):
            if img.get('src'):
                img['style'] = f"max-height:{MAX_IMAGE_HEIGHT}px;"


        content = str(soup)

        text = f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>{content}<br><br>发布时间：{published_formatted}"


        try:
           yhchat.push(PUSH_TOKEN, PUSH_GROUP, "html", {"text":text})
           print(f"已推送更新: {title}")
        except Exception as e:
            print(f"推送消息失败: {e}")

        last_entry_guid = latest_entry.guid



if __name__ == "__main__":
    print("RSS 订阅推送已启动...")

    while True:
        check_rss_updates()
        time.sleep(INTERVAL)
